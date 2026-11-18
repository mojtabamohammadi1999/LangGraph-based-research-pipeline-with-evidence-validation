
from src.llm import LLMClient


class ResearchSynthesizer:
    def __init__(self):
        self.client = LLMClient(
            temperature=0,
            max_tokens=2000,
        )


    def synthesize(
        self,
        query: str,
        facts: list[dict],
        sources: list[dict],
    ) -> str:

        # Exclude facts with zero confidence
        valid_facts = [
            fact for fact in facts
            if fact["confidence"] > 0
            and not fact.get("quote", "").strip().startswith(
                ("H1:", "H2:", "H3:", "H4:")
            )
        ]

        facts_text = "\n".join(
            f"- {fact['content']} "
            f"[Source: {fact['source_id']}] "
            f"[Confidence: {fact['confidence']}] "
            f"Quote: {fact.get('quote', '')}"
            for fact in valid_facts
        )

        sources_text = "\n".join(
            f"- {source['id']}: {source['title']} "
            f"({source['url']})"
            for source in sources
        )

        prompt = f"""
        You are an evidence-based research analyst.

        Research question:
        {query}

        Extracted facts:
        {facts_text}

        Available sources:
        {sources_text}


        Instructions:
        1. Answer the research question using only the provided facts.
        2. Every factual claim must be directly supported by
        at least one provided fact.
        3. Never introduce external knowledge, assumptions,
        or unsupported technical explanations.
        4. For comparison questions, verify that evidence exists
        for each subject being compared.
        5. If evidence exists for only one subject, explicitly
        state that a direct comparison is not possible.
        6. Never conclude that one subject is superior to another
        without supporting comparative evidence.
        7. Do not generalize benchmark results beyond their
        tested conditions.
        8. Preserve numerical values and their original context.
        9. Distinguish experimental results from hypotheses
        and recommendations.
        10. Include source references using [source-id].
        11. Mention limitations and insufficient evidence.
        12. Do not invent facts or conclusions.

        Write a concise, professional research synthesis.

        """

        return self.client.invoke(prompt)

