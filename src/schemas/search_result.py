from pydantic import BaseModel, Field, HttpUrl


class SearchResult(BaseModel):
    title: str = Field(min_length=1)
    url: HttpUrl
    content: str = ""
    score: float = Field(ge=0.0, le=1.0)