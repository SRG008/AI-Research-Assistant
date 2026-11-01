
from tavily import TavilyClient

from app.core.config import Settings


class WebSearchTool:

    def __init__(self, settings: Settings):
        self.client = TavilyClient(
            api_key=settings.tavily_api_key
        )

    def search_web(
        self,
        query: str,
        max_results: int = 8,
        topic: str = "general",
        time_range: str | None = None
    ) -> list[dict]:

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if not 1 <= max_results <= 10:
            raise ValueError("max_results must be between 1 and 10.")

        search_options = {
            "query": query,
            "max_results": max_results,
            "topic": topic
        }

        if time_range:
            search_options["time_range"] = time_range

        response = self.client.search(**search_options)

        formatted_results = []

        for result in response.get("results", []):
            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "published_date": result.get("published_date")
            })

        return formatted_results
