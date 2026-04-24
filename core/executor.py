from tools import TOOLS


def execute(tool_names: list[str], topic: str) -> list[dict]:
    articles = []
    for name in tool_names:
        tool = TOOLS.get(name)
        if not tool:
            continue
        print(f"[tool: {name}]", flush=True)
        data = tool.execute(topic)
        articles.extend(tool.build_articles(data))
    return articles
