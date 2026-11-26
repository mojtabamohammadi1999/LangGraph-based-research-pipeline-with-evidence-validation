# System Architecture

## 1. Project Overview

This project is a LangGraph-based research pipeline with evidence validation. Given a research question, it plans research tasks, searches the web, reads pages, extracts facts with supporting quotes, validates those quotes against the source text, and generates a report with source references.

The current version focuses on technology research in software engineering.

## 2. Architecture Style

The project follows a Modular Monolithic architecture.

The application runs as a single Python project, but its responsibilities are separated into independent modules. This keeps the implementation manageable while supporting testing, maintenance, and future extension.

## 3. Technology Stack

- Python 3.11
- LangGraph: workflow orchestration and state management
- LangChain: LLM integration (`ChatOpenAI`), structured output, and tool definitions
- GapGPT: OpenAI-compatible LLM API provider
- Tavily: web search
- Pydantic: data validation and schema definition
- Requests and BeautifulSoup4: web page retrieval and HTML text extraction
- pypdf: text extraction from text-based PDF documents
- Streamlit: user interface

## 4. Main Components

### 4.1 Agent (`src/agent`)

Defines the LangGraph workflow:

- `graph.py`: builds and compiles the graph
- `nodes.py`: node functions for each stage
- `state.py`: the shared state definition

### 4.2 Planner (`src/planner`)

Converts the user's question into a structured `ResearchPlan` containing research tasks, search queries, and expected information.

### 4.3 Tools (`src/tools`)

- Web Search: Tavily-based search returning `SearchResult` objects
- Web Page Reader: retrieves HTML pages and text-based PDFs and extracts readable text

Both tools are also exposed as LangChain `@tool` functions, but the current workflow calls the underlying classes directly from the nodes.

### 4.4 Research (`src/research`)

- Information Extractor: asks the LLM for facts with exact supporting quotes
- Synthesizer: produces an evidence-based analysis using only the extracted facts

Quote validation and source registration are performed in the extractor node (`src/agent/nodes.py`).

### 4.5 LLM (`src/llm`)

A thin client around `ChatOpenAI` that reads the GapGPT configuration from environment variables.

### 4.6 Schemas (`src/schemas`)

Pydantic models used across the application: `ResearchPlan`, `ResearchTask`, `SearchResult`, `PageContent`, `Fact`, `Source`, `FactExtraction`, and `Evaluation`.

### 4.7 Reporting (`src/reporting`)

Builds the final Markdown report from the synthesis, the sources, and processing errors.

### 4.8 User Interface (`app.py`)

A Streamlit application that submits the question, runs the graph, shows the report and statistics, and offers Markdown download.

## 5. Current Workflow

The workflow is a single sequential pass:

    START
      -> Planner
      -> Search
      -> Reader
      -> Information Extractor
      -> Synthesizer
      -> Report Generator
      -> END

1. Receive the user's research question.
2. Generate a structured research plan.
3. Search the web for the first tasks in the plan.
4. Read the selected pages.
5. Extract facts with supporting quotes and keep only facts whose quote exists in the page text.
6. Synthesize the validated facts.
7. Generate the final report.

## 6. Current Scope Limits

- Only the first two research tasks are searched, using the first query of each task.
- A limited number of search results and pages are processed per run.
- Only the beginning of each page is sent to the LLM for extraction.
- The workflow does not repeat research when information is missing.

## 7. Design Principles

- Separation of concerns
- Modular and maintainable code
- Structured data validation
- Source traceability
- Error handling for page retrieval and extraction
- Secure handling of API credentials through environment variables

## 8. Planned Improvements

The following items are not implemented yet:

- A research evaluator node with conditional routing back to search, limited by an iteration budget (the `Evaluation` schema already exists)
- LLM-driven tool selection using the existing tool definitions
- Automated tests and a research quality evaluation set
- FastAPI backend, Docker containerization, and deployment
