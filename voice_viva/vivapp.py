import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from flask import Flask, render_template, jsonify
from viva_speech_analyzer import SpeechAnalyzer
import json
from llm.client import chat

current_question = ""


app = Flask(__name__)

speech = SpeechAnalyzer()

@app.route("/")
def home():
    return render_template(
        "viva.html"
    )

@app.route("/generate_question")
def generate_question():

    global current_question

    with open(
        "paper_context.json",
        "r",
        encoding="utf-8"
    ) as f:

        paper_data = json.load(f)

    paper_text = paper_data[
        "paper_text"
    ][:10000]

    prompt = f"""
You are an experienced academic viva examiner.

Based on the following research paper,
ask ONE realistic viva question.

Paper:
{paper_text}

Return ONLY the question.
"""

    question = chat(
        system_prompt=
        "You are a strict academic examiner.",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    current_question = question

    return jsonify({
        "question": question
    })

@app.route("/start")
def start():

    speech.start_recording()

    return jsonify({

        "message":
        "Recording started"

    })

@app.route("/stop")
def stop():

    global current_question
    audio_file = speech.stop_recording()

    speech_data = speech.analyze(
        audio_file
    )

    transcript = speech_data["transcript"]

    evaluation_prompt = f"""
    Question:
    {current_question}

    Student Answer:
    {transcript}

    Evaluate this viva answer.

    Provide:

    1. Score out of 10
    2. Strengths
    3. Weaknesses
    4. Better Answer

    Use markdown.
    """

    evaluation = chat(
        system_prompt=
        "You are a strict academic examiner.",

        messages=[
            {
                "role":"user",
                "content":evaluation_prompt
            }
        ]
    )

    return jsonify({

        "transcript": transcript,

        "evaluation": evaluation,

        "speech_fluency":
            speech_data["speech_fluency"],

        "fillers":
            speech_data["fillers"],

        "words_per_minute":
            speech_data["words_per_minute"]

    })


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )