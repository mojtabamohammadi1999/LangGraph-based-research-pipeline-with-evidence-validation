from pydantic import BaseModel, Field

from .research_task import ResearchTask


class ResearchPlan(BaseModel):
    query: str = Field(min_length=1)
    tasks: list[ResearchTask] = Field(min_length=1)
    planning_summary: str = Field(min_length=1)