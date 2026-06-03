# llm/response_generator.py
from llm.client import chat
from llm.prompt_templates import build_system_prompt

def generate_response(
    question: str,
    chunks: list[str],
    persona_key: str,
    chat_history: list[dict]
) -> str:
    """
    Full RAG + persona response pipeline.
    
    Args:
        question: user's current question
        chunks: top-K retrieved chunks from FAISS
        persona_key: one of professor/student/skeptic/industry_expert/interviewer
        chat_history: list of {"role": ..., "content": ...} dicts
    
    Returns:
        LLM response string
    """
    system_prompt = build_system_prompt(persona_key, chunks)

    # Keep last 6 turns (3 exchanges) for conversational memory
    recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history

    messages = recent_history + [{"role": "user", "content": question}]

    return chat(system_prompt, messages)