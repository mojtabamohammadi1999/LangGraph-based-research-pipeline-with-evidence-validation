
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


class LLMClient:
    def __init__(self, temperature: float = 0.2, max_tokens: int = 2000,timeout: int = 30,max_retries: int = 0,):
        # Load environment variables from .env
        load_dotenv()

        # Read GapGPT configuration
        api_key = os.getenv("GAPGPT_API_KEY")
        base_url = os.getenv("GAPGPT_BASE_URL")
        model = os.getenv("GAPGPT_MODEL")

        # Check required configuration
        if not api_key or not base_url or not model:
            raise ValueError(
                "Missing GapGPT configuration in environment variables."
            )

        # Initialize the language model
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
        )

    def invoke(self, message: str) -> str:
        # Send the message to the language model
        response = self.llm.invoke(message)

        # Return only the response text
        return response.content
