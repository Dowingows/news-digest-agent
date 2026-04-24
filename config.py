OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

HACKERNEWS_URL = "https://hacker-news.firebaseio.com/v0"
REDDIT_URL     = "https://www.reddit.com"
DEVTO_URL      = "https://dev.to/api"

ARTICLES_PER_SOURCE = 5
MAX_CRITIC_OUTPUT   = 5

AVAILABLE_TOOLS = ["get_hackernews", "get_reddit", "get_devto"]

# Mapeamento de tópico → subreddit. Adicione novos tópicos aqui.
TOPIC_TO_SUBREDDIT = {
    "technology":              "technology",
    "artificial intelligence": "artificial",
    "machine learning":        "MachineLearning",
    "python":                  "Python",
    "programming":             "programming",
    "science":                 "science",
    "news":                    "worldnews",
    "php":                     "PHP",
    "react":                   "reactjs",
    "next":                    "nextjs",
    "nextjs":                  "nextjs",
    "javascript":              "javascript",
    "typescript":              "typescript",
    "rust":                    "rust",
    "golang":                  "golang",
    "devops":                  "devops",
    "linux":                   "linux",
    "security":                "netsec",
    "web":                     "webdev",
    "mobile":                  "mobiledev",
}
