import requests
from config import DEVTO_URL, ARTICLES_PER_SOURCE
from tools.base import Tool


class DevToTool(Tool):
    name = "get_devto"

    def execute(self, topic: str) -> list[dict]:
        tag = topic.lower().replace(" ", "")
        r = requests.get(
            f"{DEVTO_URL}/articles",
            params={"tag": tag, "per_page": ARTICLES_PER_SOURCE},
        )
        return r.json() if isinstance(r.json(), list) else []

    def build_articles(self, data: list[dict]) -> list[dict]:
        return [
            {
                "title":       article.get("title", "sem título"),
                "url":         article.get("url", ""),
                "source":      "Dev.to",
                "description": article.get("description", ""),
            }
            for article in data
        ]
