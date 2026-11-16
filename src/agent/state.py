
from typing import TypedDict

from src.schemas import Source, Fact, Evaluation, ResearchPlan


class ResearchState(TypedDict):
    user_query: str
    research_plan: ResearchPlan | None
    current_task: str

    search_results: list[dict]
    page_contents: list[dict]

    sources: list[Source]
    extracted_facts: list[Fact]
    evaluation: Evaluation | None

    missing_information: list[str]
    synthesized_findings: str | None
    final_report: str | None

    iteration_count: int
    tool_call_count: int
    errors: list[str]
    status: str