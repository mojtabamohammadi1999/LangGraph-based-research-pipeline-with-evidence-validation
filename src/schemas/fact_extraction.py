
from pydantic import BaseModel, Field


class ExtractedFact(BaseModel):
    content: str = Field(
        min_length=1,
        description="A factual statement extracted from the source."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1."
    )

    quote: str = Field(
        min_length=1,
        description="An exact supporting quote from the source."
    )


class FactExtraction(BaseModel):
    facts: list[ExtractedFact] = Field(
        default_factory=list,
        description="List of relevant facts extracted from the source."
    )
