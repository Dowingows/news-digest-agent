from tools import TOOLS
from core.debug import log_articles


def execute(tool_names: list[str], topic: str) -> list[dict]:
    articles = []
    for name in tool_names:
        tool = TOOLS.get(name)
        if not tool:
            continue
        print(f"[tool: {name}]", flush=True)
        data = tool.execute(topic)
        fetched = tool.build_articles(data)
        articles.extend(fetched)
    log_articles("EXECUTOR", articles)
    return articles
