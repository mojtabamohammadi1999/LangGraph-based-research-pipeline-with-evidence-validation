from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class Source(BaseModel):
    id: str
    url: HttpUrl
    title: str = Field(min_length=1)
    domain: str | None = None
    retrieved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    source_type: Literal[
        "web",
        "paper",
        "documentation",
        "other"
    ] = "web"