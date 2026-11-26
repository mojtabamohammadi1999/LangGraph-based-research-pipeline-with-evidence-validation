# 🔬 LangGraph-based research pipeline with evidence validation

## Overview

This project is a Python-based application designed to automate a basic research workflow using Large Language Models (LLMs), web search, and structured information extraction.

Users can submit a research question through a Streamlit interface. The agent then creates a research plan, searches the web, reads relevant pages, extracts facts with supporting quotes, synthesizes the collected evidence, and generates a research report with source references.

The project demonstrates how to build a modular AI application using LangChain, LangGraph, and external APIs.

## ✨ Features

- **Research Planning:** Breaks down research questions into structured research tasks.
- **Web Search:** Retrieves relevant web pages using Tavily Search.
- **Web Page Reading:** Extracts text from HTML pages and text-based PDF documents.
- **Structured Fact Extraction:** Extracts relevant factual statements using an LLM.
- **Supporting Quotes:** Associates extracted facts with supporting quotations from their original sources.
- **Quote Validation:** Checks whether supporting quotes exist in the original page content.
- **Evidence-Based Synthesis:** Generates research findings using the extracted facts.
- **Source References:** Includes source titles, URLs, and source identifiers in the report.
- **Research Statistics:** Displays the number of collected sources, extracted facts, and tool calls.
- **Streamlit UI:** Provides a simple interface for submitting research questions.
- **Markdown Export:** Allows users to download generated reports as Markdown files.
- **Error Handling:** Captures processing errors and displays warnings in the interface.

## 🏗️ Architecture

The application follows a modular monolithic architecture. Its research workflow is implemented using LangGraph.

### Research Workflow

```text
START
  |
  v
Planner
  |
  v
Web Search
  |
  v
Web Page Reader
  |
  v
Information Extractor
  |
  v
Research Synthesizer
  |
  v
Report Generator
  |
  v
END
```

### Workflow Description

1. **Planner:** An LLM generates a structured research plan based on the user's question.
2. **Web Search:** Tavily retrieves relevant web pages based on the research tasks.
3. **Web Page Reader:** Retrieves page content and extracts text from HTML and supported PDF documents.
4. **Information Extractor:** Identifies relevant facts and generates supporting quotes.
5. **Research Synthesizer:** Combines extracted facts into a concise research analysis.
6. **Report Generator:** Produces a Markdown research report containing findings, sources, and processing information.

LangGraph manages the workflow state and passes information between the processing nodes.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| LangChain | LLM integration and tools |
| LangGraph | Research workflow orchestration |
| GapGPT API | OpenAI-compatible LLM provider |
| Tavily | Web search |
| Pydantic | Data validation and structured schemas |
| Streamlit | Web user interface |
| BeautifulSoup4 | HTML content extraction |
| pypdf | PDF text extraction |
| Requests | HTTP requests |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
research-agent/
│
├── app.py
│
├── src/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   │
│   ├── planner/
│   │   └── planner.py
│   │
│   ├── tools/
│   │   ├── web_search.py
│   │   └── web_page_reader.py
│   │
│   ├── research/
│   │   ├── information_extractor.py
│   │   └── synthesizer.py
│   │
│   ├── reporting/
│   │   └── report_generator.py
│   │
│   ├── schemas/
│   │
│   ├── llm/
│   │   └── llm_client.py
│   │
│   └── utils/
│
├── notebooks/
├── docs/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/mojtabamohammadi1999/ai-research-agent.git
cd ai-research-agent
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository URL if necessary.

### 2. Create a Conda environment

```bash
conda create -n ai-research-agent python=3.11 -y
conda activate ai-research-agent
```

You can also use an existing Python 3.11 environment.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
GAPGPT_API_KEY=your_gapgpt_api_key
GAPGPT_BASE_URL=https://api.gapgpt.app/v1
GAPGPT_MODEL=gpt-4o-mini

TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholder values with your actual API credentials.

**API requirements:**

- A valid GapGPT API key and access to the configured model.
- A valid Tavily API key for web search.

Never commit your `.env` file or expose your API keys publicly.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

## 🚀 Usage

1. Launch the application.
2. Enter a research question in the text area.
3. Click **Start Research**.
4. Wait for the research workflow to finish.
5. Review the generated research report.
6. Check research statistics and collected sources.
7. Download the report as a Markdown file if needed.

### Example Research Question

```text
Compare FastAPI and Django in terms of performance,
scalability, and concurrency.
```

## 📊 Example Output

The generated research report contains:

- Research question
- Synthesized findings
- Referenced sources
- Research statistics
- Processing errors and warnings, when applicable

The application also displays the number of collected sources, extracted facts, and tool calls.

## ⚠️ Current Limitations

This project is an initial working implementation and has the following limitations:

- **Single-Pass Workflow:** The research workflow currently follows a linear execution path. It does not perform iterative research or automatically repeat searches based on missing information.
- **Quote Validation:** Supporting quotes are checked using exact string matching. This does not guarantee that the extracted fact is semantically supported by the quote.
- **Confidence Scores:** Confidence scores are generated by the LLM and are not independently calibrated.
- **Website Restrictions:** Some websites may block automated requests or return HTTP errors such as 403 Forbidden.
- **PDF Support:** Text extraction is supported for text-based PDF documents. OCR for scanned PDFs is not implemented.
- **Research Coverage:** Search results and extracted information depend on the availability and quality of external sources.
- **No Advanced Source Evaluation:** Comprehensive source credibility assessment and independent evidence verification are not yet implemented.

## 🔮 Future Improvements

Potential improvements include:

- Iterative research with conditional LangGraph edges.
- Advanced evidence validation and fact verification.
- Source credibility and reliability evaluation.
- Improved retry mechanisms and logging.
- Automated research quality evaluation.
- Unit and integration test coverage.
- FastAPI backend integration.
- Docker containerization.
- Cloud deployment.

## 🔐 Security

- API credentials are loaded through environment variables.
- The `.env` file should be excluded from version control.
- Never publish API keys or other sensitive credentials in the repository.

## 🎯 Project Goals

This project was developed to demonstrate practical skills in:

- Python application development.
- LLM integration through API providers.
- Structured output generation with Pydantic.
- Tool integration using LangChain.
- Workflow orchestration using LangGraph.
- Web search and information extraction.
- Evidence-based report generation.
- Building an interactive application with Streamlit.

