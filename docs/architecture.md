

\# System Architecture



\## 1. Project Overview



Tool-Using AI Research Agent is an AI-powered system designed to research and compare technologies in the field of software engineering.



The agent can plan research tasks, search for information, read web pages, extract relevant facts, evaluate collected evidence, and generate structured reports with source references.



\## 2. Architecture Style



The project follows a Modular Monolithic architecture.



The application runs as a single Python project, but its responsibilities are separated into independent modules.



This approach keeps the initial implementation manageable while supporting testing, maintenance, and future extension.



\## 3. Technology Stack



\- python 3.11

\- LangGraph: Agent workflow orchestration and state management

\- LangChain: LLM integration, prompts, tools, and structured output

\- GapGPT: LLM API provider

\- OpenAI Python SDK: API-compatible client for GapGPT

\- Pydantic: Data validation and schema definition

\- Jupyter Notebook: Experimentation and learning

\- Git: Version control



\## 4. Main Components



\### 4.1 Agent



Responsible for controlling the research workflow.



It uses LangGraph to define nodes, edges, conditional routing, and shared state.



\### 4.2 Planner



Analyzes the user's research request and converts it into a structured research plan.



\### 4.3 Tools



Provides external capabilities to the agent.



Initial tools:

\- Web Search

\- Web Page Reader



\### 4.4 Research



Responsible for:

\- Extracting relevant information

\- Validating extracted data

\- Managing research sources

\- Tracking evidence



\### 4.5 LLM



Responsible for communication with language models through GapGPT.



It separates model configuration and API communication from the rest of the application.



\### 4.6 Schemas



Defines and validates the data structures used throughout the application using Pydantic.



\### 4.7 Reporting



Combines research findings and generates structured reports with references.



\### 4.8 Utils



Contains shared helper functions that do not belong to a specific business module.



\## 5. High-Level Workflow



1\. Receive the user's research request.

2\. Process and validate the input.

3\. Generate a research plan.

4\. Search for relevant sources.

5\. Read selected web pages.

6\. Extract relevant facts and evidence.

7\. Evaluate research completeness.

8\. Repeat research when necessary, within configured limits.

9\. Synthesize collected findings.

10\. Generate the final research report.



\## 6. Design Principles



\- Separation of Concerns

\- Modular and maintainable code

\- Structured data validation

\- Source traceability

\- Controlled agent iterations

\- Error handling

\- Testability

\- Secure handling of API credentials



\## 7. Initial Scope



The first version focuses on the Core Agent System.



Web interface, FastAPI, Docker, deployment, and advanced observability are postponed until the core research workflow is functional and tested.



