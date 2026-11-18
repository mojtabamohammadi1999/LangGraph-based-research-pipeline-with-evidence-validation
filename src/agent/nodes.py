
from src.planner import Planner
from src.agent.state import ResearchState
from src.tools import WebSearchTool
from src.tools import WebPageReader
from urllib.parse import urlparse
from src.research.information_extractor import InformationExtractor
from src.schemas import Source, Fact
from src.research.synthesizer import ResearchSynthesizer
from src.reporting.report_generator import ReportGenerator


def planner_node(state: ResearchState) -> dict:
    planner = Planner()

    plan = planner.create_plan(state["user_query"])

    return {
        "research_plan": plan,
        "status": "planned",
    }


def search_node(state: ResearchState) -> dict:
    searcher = WebSearchTool(max_results=3)

    all_results = []
    plan = state["research_plan"]
    search_count = 0

    for task in plan.tasks[:2]:
        for query in task.search_queries[:1]:
            results = searcher.search(query)
            search_count += 1

            for result in results:
                all_results.append(
                    result.model_dump(mode="json")
                )

    return {
        "search_results": all_results,
        "tool_call_count": state["tool_call_count"] + search_count,
        "status": "searched",
    }


def reader_node(state: ResearchState) -> dict:
    reader = WebPageReader()

    page_contents = []
    errors = list(state["errors"])
    seen_urls = set()
    attempted_reads = 0

    for item in state["search_results"][:4]:
        url = item["url"]

        if url in seen_urls:
            continue

        seen_urls.add(url)
        attempted_reads += 1

        try:
            page = reader.read_page(url)

            page_contents.append(
                page.model_dump(mode="json")
            )

        except Exception as e:
            errors.append(f"Failed to read {url}: {str(e)}")

    return {
        "page_contents": page_contents,
        "errors": errors,
        "tool_call_count": (
            state["tool_call_count"] + attempted_reads
        ),
        "status": "read",
    }


def extractor_node(state: ResearchState) -> dict:
    extractor = InformationExtractor()
    sources = []
    extracted_facts = []
    errors = list(state["errors"])

    for index, page in enumerate(state["page_contents"]):
        try:
            url = page["url"]
            content = page["content"]

            extraction = extractor.extract(
                query=state["user_query"],
                content=content[:12000],
            )

            valid_facts = []

            for fact_index, item in enumerate(extraction.facts):
                quote = item.quote.strip()

                if not quote or quote not in content:
                    errors.append(
                        f"Rejected fact from {url}: "
                        "supporting quote not found in source."
                    )
                    continue

                fact = Fact(
                    id=f"fact-{index + 1}-{fact_index + 1}",
                    content=item.content,
                    source_id=f"source-{index + 1}",
                    confidence=item.confidence,
                    quote=quote,
                )

                valid_facts.append(fact.model_dump(mode="json"))

            if valid_facts:
                source = Source(
                    id=f"source-{index + 1}",
                    url=url,
                    title=page["title"],
                    domain=urlparse(url).netloc,
                )

                sources.append(source.model_dump(mode="json"))
                extracted_facts.extend(valid_facts)

        except Exception as e:
            errors.append(
                f"Failed to extract facts from {page['url']}: {str(e)}"
            )

    return {
        "sources": sources,
        "extracted_facts": extracted_facts,
        "errors": errors,
        "status": "extracted",
    }


def synthesis_node(state: ResearchState) -> dict:
    synthesizer = ResearchSynthesizer()

    synthesis = synthesizer.synthesize(
        query=state["user_query"],
        facts=state["extracted_facts"],
        sources=state["sources"],
    )

    return {
        "synthesized_findings": synthesis,
        "status": "synthesized",
    }

def report_node(state: ResearchState) -> dict:
    generator = ReportGenerator()

    report = generator.generate(
        query=state["user_query"],
        synthesis=state["synthesized_findings"],
        sources=state["sources"],
        errors=state["errors"],
    )

    return {
        "final_report": report,
        "status": "completed",
    }