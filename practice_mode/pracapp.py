from flask import Flask, render_template, jsonify
from video_analyzer import VideoAnalyzer
from speech_analyzer import SpeechAnalyzer
from metrics import calculate_metrics
import json
import time


app = Flask(__name__)


video = VideoAnalyzer()

speech = SpeechAnalyzer()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start")
def start():

    video.start()

    speech.start_recording()


    return jsonify({

        "message":
        "Practice started"

    })


@app.route("/stop")
def stop():


    video.stop()


    audio_file = speech.stop_recording()


    speech_data = speech.analyze(
        audio_file
    )


    video_data = video.get_metrics()



    final = calculate_metrics(
        video_data,
        speech_data
    )

    with open("results.json","w") as f:

        json.dump(
            final,
            f,
            indent=4
        )

    print(final)
    return jsonify(final)


if __name__=="__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )