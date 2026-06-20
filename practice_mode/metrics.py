def calculate_metrics(video, speech):


    total = video["total_frames"]

    face_frames = video["face_frames"]



    if total == 0:

        face_rate = 0

    else:

        face_rate = face_frames / total



    if face_frames == 0:

        eye_rate = 0

    else:

        eye_rate = (
            video["eye_contact_frames"]
            /
            face_frames
        )



    fluency = speech["speech_fluency"]



    confidence = (

        0.5 * eye_rate

        +

        0.3 * face_rate

        +

        0.2 * fluency

    )



    engagement = (

        0.6 * eye_rate

        +

        0.2 * fluency

        +

        0.2 * face_rate

    )

    total_fillers = sum(
        speech["fillers"].values()
    )

    strengths = []
    improvements = []

    if eye_rate >= 0.8:

        strengths.append(
            "Maintained strong eye contact throughout the presentation"
        )

    elif eye_rate >= 0.6:

        strengths.append(
            "Maintained reasonable eye contact"
        )

        improvements.append(
            "Try looking at the camera more consistently"
        )

    else:

        improvements.append(
            "Maintain better eye contact with the audience"
        )


    if face_rate >= 0.9:

        strengths.append(
            "Face remained clearly visible during the session"
        )

    else:

        improvements.append(
            "Stay within the camera frame throughout the presentation"
        )

    if total_fillers <= 3:

        strengths.append(
            "Spoke fluently with minimal filler words"
        )

    elif total_fillers <= 8:

        improvements.append(
            "Reduce filler words such as 'um', 'like' and 'so'"
        )

    else:

        improvements.append(
            "Excessive filler word usage detected; practice smoother delivery"
        )

    wpm = speech["words_per_minute"]

    if 100 <= wpm <= 160:

        strengths.append(
            "Maintained an effective speaking pace"
        )

    elif wpm < 100:

        improvements.append(
            "Speak slightly faster to improve engagement"
        )

    else:

        improvements.append(
            "Slow down your speaking pace for better clarity"
        )

    if confidence >= 0.85:

        strengths.append(
            "Displayed strong presentation confidence"
        )

    elif confidence < 0.65:

        improvements.append(
            "Work on confidence through additional practice sessions"
        )

    return {

    "eye_contact_rate":
    round(eye_rate*100,2),

    "face_detection_rate":
    round(face_rate*100,2),

    "filler_words":
    speech["fillers"],

    "transcript":
    speech["transcript"],

    "strengths":
    strengths,

    "improvements":
    improvements,

    "confidence_score":
    round(confidence*100,2),

    "engagement_score":
    round(engagement*100,2)

}