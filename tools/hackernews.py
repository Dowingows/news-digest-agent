import requests
from config import HACKERNEWS_URL, ARTICLES_PER_SOURCE
from tools.base import Tool


class HackerNewsTool(Tool):
    name = "get_hackernews"

    def execute(self, topic: str) -> list[dict]:
        ids = requests.get(f"{HACKERNEWS_URL}/topstories.json").json()
        articles = []
        for item_id in ids[:30]:
            item = requests.get(f"{HACKERNEWS_URL}/item/{item_id}.json").json()
            if not item or item.get("type") != "story":
                continue
            title = item.get("title", "")
            if topic.lower() in title.lower():
                articles.append(item)
            if len(articles) >= ARTICLES_PER_SOURCE:
                break
        if not articles:
            for item_id in ids[:ARTICLES_PER_SOURCE]:
                item = requests.get(f"{HACKERNEWS_URL}/item/{item_id}.json").json()
                if item and item.get("type") == "story":
                    articles.append(item)
        return articles

    def build_articles(self, data: list[dict]) -> list[dict]:
        return [
            {
                "title":  item.get("title", "sem título"),
                "url":    item.get("url", f"https://news.ycombinator.com/item?id={item.get('id')}"),
                "source": "HackerNews",
            }
            for item in data
        ]
