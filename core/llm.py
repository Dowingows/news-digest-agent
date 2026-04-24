import requests
from config import OLLAMA_URL, OLLAMA_MODEL


def call_llm(prompt: str, model: str = OLLAMA_MODEL) -> str:
    r = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False,
    })
    return r.json()["response"].strip()
