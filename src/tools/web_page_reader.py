import requests
from bs4 import BeautifulSoup
from src.schemas import PageContent
from langchain.tools import tool
from io import BytesIO
from pypdf import PdfReader

class WebPageReader:

    def __init__(self, timeout: int = 15):
        self.timeout = timeout

    def fetch_page(self, url: str) -> bytes:

        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        return response.content

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
    
    def extract_pdf_content(self, pdf_data: bytes) -> tuple[str, str]:
        pdf = PdfReader(BytesIO(pdf_data))

        title = "Untitled PDF"

        metadata = pdf.metadata
        if metadata and metadata.title:
            title = metadata.title

        content = "\n".join(
            page.extract_text() or ""
            for page in pdf.pages
        )

        return title, content

    def read_page(self, url: str) -> PageContent:
        data = self.fetch_page(url)

        if data.startswith(b"%PDF-"):
            title, content = self.extract_pdf_content(data)
        else:
            html = data.decode("utf-8", errors="replace")
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