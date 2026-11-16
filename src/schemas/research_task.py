from typing import Literal

from pydantic import BaseModel, Field


class ResearchTask(BaseModel):
    id: str
    objective: str = Field(min_length=1)
    description: str = Field(min_length=1)
    search_queries: list[str] = Field(min_length=1)
    expected_information: list[str] = Field(min_length=1)
    priority: Literal["high", "medium", "low"] = "medium"