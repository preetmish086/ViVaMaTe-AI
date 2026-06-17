import os
import re
import time
from collections import Counter
from io import BytesIO
from threading import Lock

import streamlit as st

try:
    import av
    import cv2
    import mediapipe as mp
    from streamlit_webrtc import RTCConfiguration, VideoProcessorBase, WebRtcMode, webrtc_streamer
except Exception:
    av = None
    cv2 = None
    mp = None
    RTCConfiguration = None
    VideoProcessorBase = object
    WebRtcMode = None
    webrtc_streamer = None

try:
    from groq import Groq
except Exception:
    Groq = None


FILLER_PATTERNS = {
    "um": r"\bum+\b",
    "uh": r"\buh+\b",
    "like": r"\blike\b",
    "you know": r"\byou\s+know\b",
    "actually": r"\bactually\b",
    "basically": r"\bbasically\b",
    "literally": r"\bliterally\b",
    "so": r"\bso\b",
    "right": r"\bright\b",
    "i mean": r"\bi\s+mean\b",
}

RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
) if RTCConfiguration else None


class PresentationVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.lock = Lock()
        self.total_frames = 0
        self.face_frames = 0
        self.eye_contact_frames = 0
        self.multiple_face_frames = 0
        self.last_face_count = 0
        self.started_at = time.time()

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) if mp else None

    def recv(self, frame):
        image = frame.to_ndarray(format="bgr24")

        face_count = 0
        looking_forward = False

        if self.face_mesh is not None and cv2 is not None:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb)
            faces = results.multi_face_landmarks or []
            face_count = len(faces)

            for landmarks in faces:
                h, w, _ = image.shape
                xs = [point.x for point in landmarks.landmark]
                ys = [point.y for point in landmarks.landmark]
                min_x, max_x = int(min(xs) * w), int(max(xs) * w)
                min_y, max_y = int(min(ys) * h), int(max(ys) * h)

                cv2.rectangle(
                    image,
                    (max(0, min_x), max(0, min_y)),
                    (min(w, max_x), min(h, max_y)),
                    (35, 197, 94),
                    2,
                )

                if self._is_facing_camera(landmarks):
                    looking_forward = True
                    cv2.putText(
                        image,
                        "Eye contact",
                        (max(0, min_x), max(24, min_y - 8)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (35, 197, 94),
                        2,
                    )

        with self.lock:
            self.total_frames += 1
            self.last_face_count = face_count
            if face_count > 0:
                self.face_frames += 1
            if face_count > 1:
                self.multiple_face_frames += 1
            if looking_forward:
                self.eye_contact_frames += 1

        return av.VideoFrame.from_ndarray(image, format="bgr24")

    def _is_facing_camera(self, landmarks):
        points = landmarks.landmark
        nose = points[1]
        left_cheek = points[234]
        right_cheek = points[454]
        forehead = points[10]
        chin = points[152]

        face_width = max(0.001, abs(right_cheek.x - left_cheek.x))
        face_height = max(0.001, abs(chin.y - forehead.y))
        horizontal_center = (left_cheek.x + right_cheek.x) / 2
        vertical_center = (forehead.y + chin.y) / 2

        horizontal_offset = abs(nose.x - horizontal_center) / face_width
        vertical_offset = abs(nose.y - vertical_center) / face_height

        return horizontal_offset < 0.12 and vertical_offset < 0.18

    def snapshot(self):
        with self.lock:
            total = max(1, self.total_frames)
            duration = max(1, time.time() - self.started_at)
            return {
                "duration": round(duration, 2),
                "total_frames": self.total_frames,
                "face_detection_rate": round((self.face_frames / total) * 100, 1),
                "eye_contact_rate": round((self.eye_contact_frames / total) * 100, 1),
                "multiple_face_rate": round((self.multiple_face_frames / total) * 100, 1),
                "last_face_count": self.last_face_count,
            }


def _initialize_practice_state():
    defaults = {
        "practice_started_at": None,
        "practice_last_video_metrics": {},
        "practice_transcript": "",
        "presentation_metrics": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _analyze_fillers(transcript):
    clean_text = transcript.lower().strip()
    words = re.findall(r"\b[\w']+\b", clean_text)
    word_count = len(words)

    filler_counts = {}
    total_fillers = 0
    for label, pattern in FILLER_PATTERNS.items():
        count = len(re.findall(pattern, clean_text))
        if count:
            filler_counts[label] = count
            total_fillers += count

    filler_rate = (total_fillers / max(1, word_count)) * 100
    words_per_minute = 0
    duration = st.session_state.get("practice_last_video_metrics", {}).get("duration", 0)
    if duration:
        words_per_minute = round(word_count / (duration / 60), 1)

    return {
        "word_count": word_count,
        "total_fillers": total_fillers,
        "filler_rate": round(filler_rate, 1),
        "filler_counts": filler_counts,
        "most_common_words": Counter(words).most_common(5),
        "words_per_minute": words_per_minute,
    }


def _score_practice(video_metrics, filler_metrics):
    face_score = video_metrics.get("face_detection_rate", 0)
    eye_score = video_metrics.get("eye_contact_rate", 0)
    multiple_face_penalty = min(15, video_metrics.get("multiple_face_rate", 0) / 4)

    filler_rate = filler_metrics.get("filler_rate", 0)
    filler_score = max(0, 100 - (filler_rate * 8))

    duration = video_metrics.get("duration", 0)
    duration_score = min(100, (duration / 120) * 100)

    confidence_score = (
        face_score * 0.25
        + eye_score * 0.35
        + filler_score * 0.25
        + duration_score * 0.15
        - multiple_face_penalty
    )

    return round(max(0, min(100, confidence_score)), 1)


def _build_improvements(video_metrics, filler_metrics):
    improvements = []

    if video_metrics.get("face_detection_rate", 0) < 70:
        improvements.append("Keep your face centered and well lit so the camera can consistently detect you.")

    if video_metrics.get("eye_contact_rate", 0) < 55:
        improvements.append("Look toward the camera more often, especially during key claims and conclusions.")

    if filler_metrics.get("filler_rate", 0) > 4:
        improvements.append("Reduce filler words by pausing silently between ideas instead of saying um, uh, or like.")

    if filler_metrics.get("words_per_minute", 0) > 170:
        improvements.append("Slow down slightly so technical points have time to land.")
    elif 0 < filler_metrics.get("words_per_minute", 0) < 95:
        improvements.append("Increase pace a little to sound more fluent and confident.")

    if video_metrics.get("multiple_face_rate", 0) > 10:
        improvements.append("Practice in a quieter frame with only one visible speaker.")

    if not improvements:
        improvements.append("Strong delivery. Keep practicing with the same eye contact and pacing.")

    return improvements


def _transcribe_with_groq(audio_file):
    if Groq is None:
        return ""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return ""

    client = Groq(api_key=api_key)
    audio_bytes = audio_file.getvalue()
    filename = getattr(audio_file, "name", "practice_audio.wav")

    transcription = client.audio.transcriptions.create(
        file=(filename, BytesIO(audio_bytes)),
        model="whisper-large-v3-turbo",
        response_format="text",
    )

    return transcription if isinstance(transcription, str) else str(transcription)


def _show_dependency_help():
    st.warning(
        "Live webcam analysis needs optional media packages. The app will still run, but camera tracking is disabled."
    )
    st.code(
        "pip install streamlit-webrtc av opencv-python-headless mediapipe",
        language="bash",
    )


def show_practice_mode():
    _initialize_practice_state()

    st.header("🎤 Presentation Practice")
    st.caption("Practice with live camera tracking, transcript-based filler analysis, and a confidence score.")

    if webrtc_streamer is None:
        _show_dependency_help()
    else:
        st.subheader("Live Webcam Tracking")
        st.caption("Start the camera, present normally, then stop it when you finish speaking.")

        context = webrtc_streamer(
            key="presentation-practice-camera",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIG,
            video_processor_factory=PresentationVideoProcessor,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )

        if context.state.playing and st.session_state.practice_started_at is None:
            st.session_state.practice_started_at = time.time()

        if context.video_processor:
            video_metrics = context.video_processor.snapshot()
            st.session_state.practice_last_video_metrics = video_metrics

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Duration", f"{round(video_metrics['duration'], 1)} sec")
            c2.metric("Face Detection", f"{video_metrics['face_detection_rate']}%")
            c3.metric("Eye Contact", f"{video_metrics['eye_contact_rate']}%")
            c4.metric("Faces Visible", video_metrics["last_face_count"])
        elif not st.session_state.practice_last_video_metrics:
            st.info("Camera metrics will appear once the webcam starts.")

    st.divider()
    st.subheader("Speech Transcript")

    audio_file = None
    if hasattr(st, "audio_input"):
        audio_file = st.audio_input("Record your speech for transcription")

    if audio_file and st.button("Transcribe Audio", use_container_width=True):
        with st.spinner("Transcribing audio..."):
            try:
                transcript = _transcribe_with_groq(audio_file)
                if transcript:
                    st.session_state.practice_transcript = transcript
                    st.success("Transcript generated.")
                else:
                    st.warning("Automatic transcription is unavailable. Paste your transcript below.")
            except Exception as exc:
                st.warning(f"Could not transcribe audio automatically: {exc}")

    transcript = st.text_area(
        "Paste or edit what you said",
        value=st.session_state.practice_transcript,
        height=180,
        placeholder="Paste your presentation transcript here to calculate filler words...",
    )
    st.session_state.practice_transcript = transcript

    if st.button("Generate Practice Report", type="primary", use_container_width=True):
        video_metrics = st.session_state.practice_last_video_metrics or {
            "duration": 0,
            "face_detection_rate": 0,
            "eye_contact_rate": 0,
            "multiple_face_rate": 0,
            "last_face_count": 0,
        }
        filler_metrics = _analyze_fillers(transcript)
        confidence_score = _score_practice(video_metrics, filler_metrics)
        improvements = _build_improvements(video_metrics, filler_metrics)

        st.session_state.presentation_metrics = {
            **video_metrics,
            **filler_metrics,
            "confidence_score": confidence_score,
            "engagement_score": round(
                (
                    video_metrics.get("eye_contact_rate",0) * 0.7
                    +
                    video_metrics.get("face_detection_rate",0) * 0.3
                ),
                1
            ),            
            "presentation_score": confidence_score,
            "areas_to_improve": improvements,
        }

    metrics = st.session_state.get("presentation_metrics", {})
    if metrics:
        st.success("Practice report ready. Metrics are saved for the Final Report tab.")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Confidence", f"{metrics.get('confidence_score', 0)}%")
        m2.metric("Eye Contact", f"{metrics.get('eye_contact_rate', 0)}%")
        m3.metric("Face Detection", f"{metrics.get('face_detection_rate', 0)}%")
        m4.metric("Filler Words", metrics.get("total_fillers", 0))

        st.markdown("### Filler Word Breakdown")
        filler_counts = metrics.get("filler_counts", {})
        if filler_counts:
            for filler, count in filler_counts.items():
                st.write(f"**{filler}**: {count}")
        else:
            st.write("No major filler words detected in the transcript.")

        st.markdown("### Areas To Improve")
        for item in metrics.get("areas_to_improve", []):
            st.warning(item)
