# Data Flow Design

## 1. Overview

A research request moves through a sequence of stages. Each stage reads the shared agent state, performs one task, and writes its results back to the state. LangGraph controls the order of execution.

## 2. Current Execution Flow

    START
      -> Planner
      -> Search
      -> Reader
      -> Information Extractor
      -> Synthesizer
      -> Report Generator
      -> END

The flow is linear. There is no conditional routing in the current version.

## 3. Node Responsibilities

### Planner

- Input: `user_query`
- Output: `research_plan`
- Uses the LLM with structured output to produce a `ResearchPlan` with tasks, search queries, expected information, and priorities.

### Search

- Input: `research_plan`
- Output: `search_results`, updated `tool_call_count`
- Searches the first two tasks, using the first query of each task.
- Uses Tavily with basic search depth and a small number of results per query.

### Reader

- Input: `search_results`
- Output: `page_contents`, `errors`, updated `tool_call_count`
- Processes a limited number of results and skips duplicate URLs.
- Fetches each page and extracts text from HTML or from text-based PDFs.
- A page that cannot be retrieved is recorded in `errors` and does not stop the workflow.

### Information Extractor

- Input: `page_contents`, `user_query`
- Output: `sources`, `extracted_facts`, `errors`
- Sends the beginning of each page to the LLM and receives structured facts, each with a supporting quote and a confidence score.
- Rejects a fact when its quote is not found in the page text (exact string matching).
- Registers a source only when at least one of its facts is valid.
- Fact IDs and source IDs are generated from page and fact positions (for example `fact-1-2`, `source-1`).

### Synthesizer

- Input: `extracted_facts`, `sources`, `user_query`
- Output: `synthesized_findings`
- Excludes facts with zero confidence.
- The prompt restricts the LLM to the provided facts and requires source references and a statement of limitations.

### Report Generator

- Input: `synthesized_findings`, `sources`, `errors`
- Output: `final_report`
- Builds a Markdown report with the question, findings, sources, research status, and processing errors.

## 4. Error Handling

- Page retrieval failures and extraction failures are recorded per page in `errors`, and processing continues with the remaining pages.
- Rejected facts are also recorded in `errors`.
- Failures in planning, search, synthesis, or the LLM connection are not caught inside the nodes. They propagate to the Streamlit application, which displays an error message.
- The LLM client currently does not retry failed requests.

## 5. Data Integrity

- Every extracted fact references its source through `source_id` and keeps its supporting quote.
- Duplicate URLs are skipped in the reader stage.
- Facts whose quote cannot be found in the source are not used.
- Quote validation checks only that the quote exists in the page text. It does not verify that the fact is semantically supported by the quote.

## 6. Planned Flow

The following flow is planned but not implemented:

    Planner -> Search -> Reader -> Information Extractor -> Research Evaluator
                  ^                                               |
                  |------------ insufficient information --------|
                                                                  |
                                           sufficient or limit reached
                                                                  v
                                                    Synthesizer -> Report Generator

- The Research Evaluator would use the `Evaluation` schema to decide whether more research is needed.
- Missing information would drive new search queries.
- Iteration and tool-call limits would stop the loop and let the report state its limitations.
