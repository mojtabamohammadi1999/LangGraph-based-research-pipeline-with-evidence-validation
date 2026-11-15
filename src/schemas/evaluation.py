from typing import Literal

from pydantic import BaseModel, Field


class Evaluation(BaseModel):
    is_sufficient: bool
    reason: str = Field(min_length=1)
    missing_information: list[str] = Field(default_factory=list)
    recommended_next_action: Literal[
        "search",
        "synthesize",
        "stop"
    ]