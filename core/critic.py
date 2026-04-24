import json
import re
from config import MAX_CRITIC_OUTPUT
from core.llm import call_llm
from core.debug import log_prompt, log_response, log_articles

CRITIC_PROMPT = """Você é um editor crítico de notícias.
Filtre a lista abaixo e selecione os {max} artigos mais relevantes para o tópico "{topic}".
Retorne APENAS um JSON array com os índices dos artigos selecionados, sem texto adicional.
Exemplo: [0, 2, 4]

ARTIGOS:
{articles_list}"""


def filter_articles(articles: list[dict], topic: str) -> list[dict]:
    if not articles:
        return []

    numbered = "\n".join(
        f"{i}. [{a['source']}] {a['title']}" for i, a in enumerate(articles)
    )

    prompt = CRITIC_PROMPT.format(
        max=MAX_CRITIC_OUTPUT,
        topic=topic,
        articles_list=numbered,
    )

    log_prompt("CRITIC", prompt)
    response = call_llm(prompt)
    log_response("CRITIC", response)

    match = re.search(r'\[[\d,\s]+\]', response)
    if not match:
        return articles[:MAX_CRITIC_OUTPUT]

    try:
        indices = json.loads(match.group())
        selected = [articles[i] for i in indices if 0 <= i < len(articles)]
        result = selected[:MAX_CRITIC_OUTPUT] if selected else articles[:MAX_CRITIC_OUTPUT]
        log_articles("CRITIC (selecionados)", result)
        return result
    except (json.JSONDecodeError, IndexError):
        return articles[:MAX_CRITIC_OUTPUT]
