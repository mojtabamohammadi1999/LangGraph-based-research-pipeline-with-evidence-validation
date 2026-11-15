from pydantic import BaseModel, Field


class Fact(BaseModel):
    id: str
    content: str = Field(min_length=1)
    source_id: str
    confidence: float = Field(ge=0.0, le=1.0)
    quote: str | None = None