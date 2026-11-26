# State Design

## 1. Overview

The Agent State is the shared data structure used to maintain information throughout the research workflow.

Each LangGraph node reads the information it needs from the State and updates the relevant fields.

The State is responsible for maintaining research progress, collected evidence, execution metadata, and final outputs.

## 2. State Structure

Fields marked **(reserved)** are defined in the State but are not used by the current linear workflow. They are prepared for a future iterative version.

### 2.1 Input Fields

| Field | Type | Description |
|---|---|---|
| `user_query` | `str` | Original research request submitted by the user |

### 2.2 Planning Fields

| Field | Type | Description |
|---|---|---|
| `research_plan` | `ResearchPlan` or `None` | Structured research plan containing a list of research tasks |
| `current_task` | `str` | **(reserved)** Research task currently being executed |

### 2.3 Execution Fields

| Field | Type | Description |
|---|---|---|
| `search_results` | `list[dict]` | Results collected from web searches |
| `page_contents` | `list[dict]` | Content retrieved from web pages |

### 2.4 Evidence Fields

| Field | Type | Description |
|---|---|---|
| `sources` | `list[dict]` | Registered research sources (serialized `Source` models) |
| `extracted_facts` | `list[dict]` | Validated facts extracted from sources (serialized `Fact` models) |

### 2.5 Evaluation Fields

| Field | Type | Description |
|---|---|---|
| `evaluation` | `Evaluation` or `None` | **(reserved)** Structured assessment of research completeness |
| `missing_information` | `list[str]` | **(reserved)** Information that is still missing |

These fields are intended for a future research evaluator that decides whether another search iteration is needed.

### 2.6 Output Fields

| Field | Type | Description |
|---|---|---|
| `synthesized_findings` | `str` or `None` | Combined research findings |
| `final_report` | `str` or `None` | Final generated research report |

### 2.7 Execution Control Fields

| Field | Type | Description |
|---|---|---|
| `iteration_count` | `int` | **(reserved)** Number of research iterations |
| `tool_call_count` | `int` | Number of search and page-read operations |
| `errors` | `list[str]` | Errors encountered during execution |
| `status` | `str` | Current workflow status |

## 3. State Status Values

The workflow sets the status value at the end of each node:

- `initialized`: the initial State has been created.
- `planned`: the research plan has been generated.
- `searched`: web search has finished.
- `read`: web pages have been retrieved.
- `extracted`: facts have been extracted and validated.
- `synthesized`: findings have been synthesized.
- `completed`: the final report has been generated.

Unhandled failures are raised as exceptions and are handled by the Streamlit application; they are not stored in the State.

## 4. Data Modeling Strategy

The project uses a combination of TypedDict and Pydantic.

- TypedDict defines the main LangGraph State structure.
- Pydantic models (`Source`, `Fact`, `ResearchPlan`, `Evaluation`) define and validate structured data.
- `Source` and `Fact` are converted to dictionaries with `model_dump` before being stored in the State, which keeps the State simple and serializable.
- `Evaluation` is defined but not used yet.

## 5. State Update Strategy

Each node updates only the fields relevant to its responsibility:

- Planner updates `research_plan`.
- Search updates `search_results` and `tool_call_count`.
- Reader updates `page_contents`, `errors`, and `tool_call_count`.
- Information Extractor updates `sources`, `extracted_facts`, and `errors`.
- Synthesizer updates `synthesized_findings`.
- Report Generator updates `final_report`.

Every node also updates `status`.

The current workflow is a sequential single pass. State reducers can be introduced if iterative or parallel execution is added later.

## 6. Design Principles

- Keep the State simple and explicit.
- Validate structured data with Pydantic when it is created.
- Preserve the relationship between extracted facts and their sources.
- Track execution progress and errors.
- Avoid unnecessary duplication of information.
- Support future extensions without complicating the initial implementation.
