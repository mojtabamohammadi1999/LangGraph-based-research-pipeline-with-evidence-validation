
from src.llm import LLMClient
from src.schemas import FactExtraction


class InformationExtractor:

    def __init__(self):
        self.client = LLMClient(
            temperature=0,
            max_tokens=2000,
        )

        self.structured_llm = self.client.llm.with_structured_output(
            FactExtraction,
            method="function_calling",
        )

    def extract(self, query: str, content: str) -> FactExtraction:

        prompt = f"""
        You are an expert research information extractor.

        Your task is to extract important factual information
        from the provided web page.

        Research question:
        {query}

        Web page content:
        {content}

        Instructions:
        1. Extract only facts relevant to the research question.
        2. Each fact must contain one clear factual statement.
        3. Provide an exact supporting quote from the content.
        4. Assign a confidence score between 0 and 1.
        5. Do not invent information.
        6. If no relevant facts exist, return an empty list.
        """

        result = self.structured_llm.invoke(prompt)

        return result
