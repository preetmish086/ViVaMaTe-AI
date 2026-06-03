# utils/memory.py

def add_turn(history: list[dict], role: str, content: str) -> list[dict]:
    """Append a turn to chat history."""
    history.append({"role": role, "content": content})
    return history

def get_recent(history: list[dict], n_turns: int = 6) -> list[dict]:
    """Return last n messages."""
    return history[-n_turns:] if len(history) > n_turns else history

def clear_history() -> list:
    return []