import json
import re
from config import AVAILABLE_TOOLS
from core.llm import call_llm

PLANNER_PROMPT = """Você é um planejador de busca de notícias.
Fontes disponíveis: {tools}
Com base no pedido, decida quais fontes usar e extraia o tópico principal em inglês (para buscas nas APIs).
Retorne APENAS JSON, sem texto adicional.
Exemplo: {{"tools": ["get_hackernews", "get_devto"], "topic": "artificial intelligence"}}
Pedido: {user_input}"""


def plan(user_input: str) -> dict:
    prompt = PLANNER_PROMPT.format(
        tools=", ".join(AVAILABLE_TOOLS),
        user_input=user_input,
    )
    response = call_llm(prompt)

    match = re.search(r'\{.*\}', response, re.DOTALL)
    if not match:
        return {"tools": ["get_hackernews"], "topic": user_input}

    try:
        result = json.loads(match.group())
        if "tools" not in result or "topic" not in result:
            raise ValueError
        result["tools"] = [t for t in result["tools"] if t in AVAILABLE_TOOLS]
        if not result["tools"]:
            result["tools"] = ["get_hackernews"]
        return result
    except (json.JSONDecodeError, ValueError):
        return {"tools": ["get_hackernews"], "topic": user_input}
