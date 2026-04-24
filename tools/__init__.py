from tools.hackernews import HackerNewsTool
from tools.reddit import RedditTool
from tools.devto import DevToTool

TOOLS = {
    "get_hackernews": HackerNewsTool(),
    "get_reddit":     RedditTool(),
    "get_devto":      DevToTool(),
}
