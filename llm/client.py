import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant" # free, fast, good quality
# Alternative: "mixtral-8x7b-32768" — better reasoning, larger context

def chat(system_prompt: str, messages: list[dict], max_tokens: int = 1024) -> str:
    """
    Send a RAG-augmented chat request to Groq.
    messages = list of {"role": "user"/"assistant", "content": "..."}
    """
    try:
        response = _client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content

    except Exception as e:
        err = str(e).lower()
        if "authentication" in err or "api key" in err:
            return "⚠️ Invalid GROQ_API_KEY. Check your .env file."
        elif "rate limit" in err:
            return "⚠️ Rate limit hit. Wait a few seconds and retry."
        elif "connection" in err:
            return "⚠️ No internet connection."
        else:
            return f"⚠️ Error: {str(e)}"