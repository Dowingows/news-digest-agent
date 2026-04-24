import os

DEBUG = os.getenv("DEBUG", "0") == "1"

_BORDER = "─" * 60


def log_prompt(stage: str, prompt: str) -> None:
    if not DEBUG:
        return
    print(f"\n\033[33m┌── PROMPT [{stage}] {'─' * (50 - len(stage))}\033[0m")
    for line in prompt.strip().splitlines():
        print(f"\033[33m│\033[0m  {line}")
    print(f"\033[33m└{_BORDER}\033[0m\n")


def log_response(stage: str, response: str) -> None:
    if not DEBUG:
        return
    print(f"\033[32m┌── RESPOSTA [{stage}] {'─' * (48 - len(stage))}\033[0m")
    for line in response.strip().splitlines():
        print(f"\033[32m│\033[0m  {line}")
    print(f"\033[32m└{_BORDER}\033[0m\n")


def log_articles(stage: str, articles: list[dict]) -> None:
    if not DEBUG:
        return
    print(f"\033[36m┌── ARTIGOS [{stage}] ({len(articles)} itens) {'─' * (40 - len(stage))}\033[0m")
    for i, a in enumerate(articles):
        desc = f" — {a['description'][:60]}" if a.get("description") else ""
        print(f"\033[36m│\033[0m  {i}. [{a['source']}] {a['title'][:60]}{desc}")
    print(f"\033[36m└{_BORDER}\033[0m\n")
