import requests
from config import REDDIT_URL, ARTICLES_PER_SOURCE, TOPIC_TO_SUBREDDIT
from tools.base import Tool

HEADERS = {"User-Agent": "news-digest-agent/1.0"}


def _subreddit_for(topic: str) -> str:
    lower = topic.lower()
    for key, sub in TOPIC_TO_SUBREDDIT.items():
        if key in lower:
            return sub
    return "technology"


class RedditTool(Tool):
    name = "get_reddit"

    def execute(self, topic: str) -> list[dict]:
        sub = _subreddit_for(topic)
        r = requests.get(
            f"{REDDIT_URL}/r/{sub}/hot.json",
            params={"limit": ARTICLES_PER_SOURCE},
            headers=HEADERS,
        )
        posts = r.json().get("data", {}).get("children", [])
        return [p["data"] for p in posts if not p["data"].get("is_self")]

    def build_articles(self, data: list[dict]) -> list[dict]:
        return [
            {
                "title":       post.get("title", "sem título"),
                "url":         post.get("url", f"https://reddit.com{post.get('permalink', '')}"),
                "source":      "Reddit",
                "description": f"r/{post.get('subreddit', '')} · {post.get('score', 0)} upvotes · {int(post.get('upvote_ratio', 0) * 100)}% positivo",
            }
            for post in data
        ]
