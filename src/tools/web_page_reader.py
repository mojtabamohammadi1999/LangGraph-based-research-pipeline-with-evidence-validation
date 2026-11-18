import requests
from bs4 import BeautifulSoup
from src.schemas import PageContent
from langchain.tools import tool

class WebPageReader:

    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    def fetch_page(self, url: str) -> str:

        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        return response.text

    def extract_content(self, html: str) -> tuple[str, str]:

        soup = BeautifulSoup(html, "html.parser")

        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "Untitled Page"
        )

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
        ]):
            element.decompose()

        content = soup.get_text(separator=" ", strip=True)

        return title, content

    def read_page(self, url: str) -> PageContent:

        html = self.fetch_page(url)

        title, content = self.extract_content(html)

        page = PageContent(
            url=url,
            title=title,
            content=content,
            word_count=len(content.split()),
        )

        return page

@tool
def read_web_page(url: str) -> dict:
    """Read a web page and extract its title and text content."""

    reader = WebPageReader()

    page = reader.read_page(url)

    return page.model_dump(mode="json")