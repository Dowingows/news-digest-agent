from core.llm import call_llm
from core.debug import log_prompt, log_response

REPORT_PROMPT = """Gere um digest de notícias conciso em português sobre "{topic}".
Use bullets (•), máximo 8 linhas no total. Para cada artigo inclua o título traduzido e o link.
Seja direto, sem introdução longa.

ARTIGOS SELECIONADOS:
{articles}

PEDIDO ORIGINAL: {user_input}"""


def respond(user_input: str, topic: str, articles: list[dict]) -> str:
    formatted = "\n".join(
        f"- {a['title']} ({a['source']}) — {a['url']}" for a in articles
    )
    prompt = REPORT_PROMPT.format(
        topic=topic,
        articles=formatted,
        user_input=user_input,
    )
    log_prompt("RESPONDER", prompt)
    response = call_llm(prompt)
    log_response("RESPONDER", response)
    return response
