

\# Data Flow Design



\## 1. Overview



The research agent processes a user request through a sequence of interconnected stages.



Each stage performs a specific task and passes its results through the shared agent state.



LangGraph controls the execution flow between these stages.



\## 2. Main Execution Flow



START

&#x20; |

&#x20; v

Input Processing

&#x20; |

&#x20; v

Planner

&#x20; |

&#x20; v

Search

&#x20; |

&#x20; v

Reader

&#x20; |

&#x20; v

Information Extractor

&#x20; |

&#x20; v

Research Evaluator

&#x20; |

&#x20; +---- Insufficient Information ----> Search

&#x20; |

&#x20; +---- Sufficient Information ------> Synthesis

&#x20;                                         |

&#x20;                                         v

&#x20;                                   Report Generation

&#x20;                                         |

&#x20;                                         v

&#x20;                                        END



\## 3. Node Responsibilities



\### Input Processing Node



Input:

\- Raw user request



Output:

\- Validated user query



Responsibilities:

\- Receive the user's research request.

\- Validate that the request is not empty.

\- Prepare the initial agent state.



\### Planner Node



Input:

\- User query



Output:

\- Structured research plan



Responsibilities:

\- Understand the research objective.

\- Identify important research dimensions.

\- Generate smaller research tasks.

\- Define the information needed for each task.



\### Search Node



Input:

\- Research plan

\- Current research task



Output:

\- Search results



Responsibilities:

\- Search for relevant sources.

\- Collect URLs and source metadata.

\- Prefer official documentation and primary sources.



\### Reader Node



Input:

\- Selected source URLs



Output:

\- Retrieved page contents



Responsibilities:

\- Retrieve web page content.

\- Extract readable text.

\- Handle inaccessible pages and retrieval errors.



\### Information Extractor Node



Input:

\- Page contents

\- Current research task



Output:

\- Structured facts and evidence



Responsibilities:

\- Extract relevant information.

\- Associate extracted facts with their sources.

\- Validate extracted data structures.



\### Research Evaluator Node



Input:

\- Research plan

\- Extracted facts

\- Source information



Output:

\- Evaluation result and next action



Responsibilities:

\- Check research completeness.

\- Identify missing information.

\- Decide whether another research iteration is necessary.



Possible decisions:

\- Continue research.

\- Proceed to synthesis.

\- Stop because of an error or iteration limit.



\### Synthesis Node



Input:

\- Collected facts and evidence

\- Source registry



Output:

\- Synthesized findings



Responsibilities:

\- Combine findings from different sources.

\- Identify agreements and contradictions.

\- Preserve evidence references.

\- Prepare conclusions.



\### Report Generation Node



Input:

\- Synthesized findings

\- Source registry



Output:

\- Final research report



Responsibilities:

\- Generate a structured report.

\- Include citations and source references.

\- Present conclusions and limitations.



\## 4. Conditional Routing



The Research Evaluator determines the next stage.



If the collected information is insufficient:

\- Return to Search.

\- Focus on missing research dimensions.

\- Increment the research iteration counter.



If the information is sufficient:

\- Continue to Synthesis.



If the maximum iteration limit is reached:

\- Stop additional research.

\- Continue with available evidence, clearly reporting limitations.



\## 5. Error Handling



Errors must be tracked separately from research completeness.



Examples:

\- Search provider unavailable.

\- Page retrieval failed.

\- Invalid model response.

\- Structured output validation failed.



Recoverable errors may be retried within configured limits.



Unrecoverable errors should be recorded and handled through a controlled termination path.



\## 6. Execution Limits



Initial configuration:



\-Maximum research iterations: 10

\-Maximum tool calls:15



These values are configurable and may be adjusted during evaluation.



\## 7. Data Integrity



\- Each extracted fact should reference its supporting source.

\- Duplicate sources should be detected.

\- Source metadata should be preserved.

\- Unsupported claims must not be presented as verified facts.



