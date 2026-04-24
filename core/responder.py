from core.llm import call_llm
from core.debug import log_prompt, log_response

REPORT_PROMPT = """Você é editor de uma newsletter técnica semanal em português.
Escreva um digest no estilo newsletter sobre "{topic}" com base nos artigos abaixo.

Para cada artigo use este formato exato:

### [Título em português]
[Uma frase resumindo o que é o artigo, baseada no título e descrição]
📰 {{fonte}} · 🔗 {{url}}

---

Regras:
- Traduza os títulos para português
- O resumo deve ser informativo, não genérico ("este artigo fala sobre X")
- Se a descrição estiver vazia, infira pelo título
- Não adicione introdução nem conclusão

ARTIGOS:
{articles}"""


def respond(user_input: str, topic: str, articles: list[dict]) -> str:
    formatted = "\n\n".join(
        f"Título: {a['title']}\nDescrição: {a.get('description', '')}\nFonte: {a['source']}\nURL: {a['url']}"
        for a in articles
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
