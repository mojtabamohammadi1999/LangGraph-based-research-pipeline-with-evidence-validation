

\# State Design



\## 1. Overview



The Agent State is the shared data structure used to maintain information throughout the research workflow.



Each LangGraph node reads the information it needs from the State and updates the relevant fields.



The State is responsible for maintaining research progress, collected evidence, execution metadata, and final outputs.



\## 2. State Structure



The initial State contains the following groups of fields.



\### 2.1 Input Fields



| Field | Type | Description |

|---|---|---|

| user\_query | str | Original research request submitted by the user |



\### 2.2 Planning Fields



| Field | Type | Description |

|---|---|---|

| research\_plan | list | Structured list of research tasks |

| current\_task | str | Research task currently being executed |



\### 2.3 Execution Fields



| Field | Type | Description |

|---|---|---|

| search\_results | list | Results collected from web searches |

| page\_contents | list | Content retrieved from web pages |



\### 2.4 Evidence Fields



| Field | Type | Description |

|---|---|---|

| sources | list | Registered research sources |

| extracted\_facts | list | Facts and evidence extracted from sources |



\### 2.5 Evaluation Fields



| Field | Type | Description |

|---|---|---|

| evaluation | Evaluation | Structured assessment of research completeness |

| missing\_information | list | Information that is still missing |



\### 2.6 Output Fields



| Field | Type | Description |

|---|---|---|

| synthesized\_findings | str or None | Combined research findings |

| final\_report | str or None | Final generated research report |



\### 2.7 Execution Control Fields



| Field | Type | Description |

|---|---|---|

| iteration\_count | int | Number of research iterations |

| tool\_call\_count | int | Number of tool executions |

| errors | list | Errors encountered during execution |

| status | str | Current workflow status |



\## 3. State Status Values



The initial workflow uses the following status values:



\- pending: Research has not started.

\- running: Research is currently in progress.

\- completed: Research has finished successfully.

\- failed: Research could not be completed.



\## 4. Data Modeling Strategy



The project uses a combination of TypedDict and Pydantic.



\- TypedDict defines the main LangGraph State structure.

\- Pydantic models define and validate structured data stored inside the State.

\- Source, Fact, and Evaluation will be implemented as structured models.



This approach keeps the Graph State simple while maintaining data validation.


\## 5. State Update Strategy



Each node updates only the fields relevant to its responsibility.



For example:



\- Planner updates research\_plan and current\_task.

\- Search updates search\_results.

\- Reader updates page\_contents.

\- Information Extractor updates sources and extracted\_facts.

\- Research Evaluator updates evaluation and missing\_information.

\- Report Generation updates final\_report.



The initial workflow is sequential. More advanced state merging and reducers can be introduced if parallel execution is added later.



\## 6. Design Principles



\- Keep the State simple and explicit.

\- Use structured data instead of unrestricted dictionaries where possible.

\- Preserve the relationship between extracted facts and their sources.

\- Track execution progress and errors.

\- Avoid unnecessary duplication of information.

\- Support future extensions without complicating the initial implementation.



