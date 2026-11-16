from src.llm import LLMClient
from src.schemas import ResearchPlan


class Planner:

    def __init__(self):
        self.client = LLMClient(
            temperature=0,
            max_tokens=2000,
        )

        self.structured_llm = self.client.llm.with_structured_output(
            ResearchPlan,
            method="function_calling",
        )

    def create_plan(self, query: str) -> ResearchPlan:

        prompt = f"""
        You are an expert research planner.

        Your task is to create a structured research plan
        based on the user's research question.

        User query:
        {query}

        Instructions:
        1. Break down the research question into clear tasks.
        2. Each task must have specific search queries.
        3. Define the expected information for each task.
        4. Assign a priority to each task.
        5. Provide a short planning summary.
        6. Ensure that all important aspects of the
           research question are covered.
        """

        plan = self.structured_llm.invoke(prompt)

        return plan    