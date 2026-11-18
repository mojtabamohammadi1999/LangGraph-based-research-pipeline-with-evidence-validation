from pydantic import BaseModel, Field, HttpUrl


class PageContent(BaseModel):
    url: HttpUrl
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)
    word_count: int = Field(ge=0)