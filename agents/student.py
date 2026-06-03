# agents/professor.py
from llm.response_generator import generate_response

def respond(question: str, chunks: list[str], chat_history: list[dict]) -> str:
    return generate_response(question, chunks, "student", chat_history)