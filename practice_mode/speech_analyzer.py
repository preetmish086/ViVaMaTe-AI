import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import threading
import time
import os
import re
import numpy as np


class SpeechAnalyzer:


    def __init__(self):

        print("Loading Whisper model...")

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

        print("Whisper ready")

        self.recording = False
        self.audio = []
        self.thread = None

        self.sample_rate = 16000

        self.filename = "practice_audio.wav"



    def start_recording(self):

        self.recording = True
        self.audio = []

        self.thread = threading.Thread(
            target=self.record
        )

        self.thread.start()



    def record(self):

        def callback(indata, frames, time_info, status):

            if status:
                print(status)

            if self.recording:
                self.audio.extend(indata.copy())



        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=callback
        ):

            while self.recording:

                time.sleep(0.1)




    def stop_recording(self):

        self.recording = False

        if self.thread:
            self.thread.join()

        audio_data = np.array(
            self.audio,
            dtype=np.float32
        )

        print("Recorded samples:", len(audio_data))
        print("Audio shape:", audio_data.shape)

        if len(audio_data) > 0:

            write(
                self.filename,
                self.sample_rate,
                audio_data
            )

            print("Audio saved")

        else:

            print("No audio recorded")

        return self.filename




    def analyze(self, filename):


        # model = WhisperModel(
        #     "base",
        #     compute_type="int8"
        # )


        segments, info = self.model.transcribe(
            filename
        )


        transcript=""


        for segment in segments:

            transcript += segment.text+" "



        transcript = transcript.lower()



        fillers=[

            "um",
            "uh",
            "like",
            "basically",
            "actually",
            "you know",
            "so"

        ]


        counts={}


        for word in fillers:

            counts[word] = len(
                re.findall(
                    re.escape(word),
                    transcript
                )
            )

        total_fillers = sum(
            counts.values()
        )


        duration = info.duration



        # simple fluency score

        words=len(
            transcript.split()
        )


        if duration>0:

            words_per_minute = (
                words/duration
            )*60

        else:

            words_per_minute=0



        if words > 0:

            filler_ratio = (
                total_fillers / words
            )

        else:

            filler_ratio = 0


        if 90 <= words_per_minute <= 160:

            fluency = 1

        else:

            fluency = 0.8


        fluency = max(
            0.5,
            fluency - (filler_ratio * 2)
        )

        print("\nTranscript:")
        print(transcript)
        print("\nFillers:")
        print(counts)


        return {


            "duration":
            round(duration,2),


            "speech_fluency":
            fluency,


            "fillers":
            counts,


            "transcript":
            transcript,

            "words_per_minute": round(
                words_per_minute,
                1
            )
        }