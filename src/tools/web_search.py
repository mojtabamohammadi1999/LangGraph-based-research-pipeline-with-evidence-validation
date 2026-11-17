from langchain_tavily import TavilySearch
from src.schemas import SearchResult
from langchain.tools import tool

class WebSearchTool:

    def __init__(self, max_results: int = 5):
        self.search_tool = TavilySearch(
            max_results=max_results,
            topic="general",
            search_depth="basic",
        )

    def search(self, query: str) -> list[SearchResult]:

        response = self.search_tool.invoke({
            "query": query
        })

        search_results = [
            SearchResult(
                title=item["title"],
                url=item["url"],
                content=item.get("content", ""),
                score=item["score"],
            )
            for item in response["results"]
        ]

        return search_results


@tool
def web_search(query: str) -> list[dict]:
    """Search the web for information about a given query."""

    search_tool = WebSearchTool()

    results = search_tool.search(query)

    return [
        result.model_dump(mode="json")
        for result in results
    ]