class ReportGenerator:

    def generate(
        self,
        query: str,
        synthesis: str,
        sources: list[dict],
        errors: list[str],
    ) -> str:

        sources_text = "\n".join(
            f"{index}. **{source['title']}**\n"
            f"   - URL: {source['url']}\n"
            f"   - Source ID: {source['id']}"
            for index, source in enumerate(sources, start=1)
        )

        report = f"""# Research Report

## Research Question

{query}

## Findings

{synthesis}

## Sources

{sources_text}

## Research Status

- Sources collected: {len(sources)}
- Errors encountered: {len(errors)}

"""

        if errors:
            report += "\n## Processing Errors\n"
            report += "\n".join(f"- {error}" for error in errors)

        return report