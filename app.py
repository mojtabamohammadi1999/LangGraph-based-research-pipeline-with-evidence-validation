
import streamlit as st
from dotenv import load_dotenv

from src.agent.graph import graph

load_dotenv()

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 AI Research Agent")

st.markdown(
    """
    An AI-powered research assistant that searches the web,
    extracts relevant facts, and generates evidence-based reports.
    """
)

st.divider()

st.subheader("Start a New Research")

user_query = st.text_area(
    "Enter your research question:",
    placeholder="Example: Compare FastAPI and Django in terms of performance and scalability.",
    height=120,
)

if st.button("Start Research", type="primary"):
    if not user_query.strip():
        st.warning("Please enter a research question.")

    else:
        initial_state = {
            "user_query": user_query.strip(),
            "research_plan": None,
            "current_task": "",
            "search_results": [],
            "page_contents": [],
            "sources": [],
            "extracted_facts": [],
            "evaluation": None,
            "missing_information": [],
            "synthesized_findings": None,
            "final_report": None,
            "iteration_count": 0,
            "tool_call_count": 0,
            "errors": [],
            "status": "initialized",
        }

        try:
            with st.spinner(
                "Research Agent is working... Please wait."
            ):
                final_state = graph.invoke(initial_state)

            st.success("Research completed successfully!")

            st.subheader("Research Report")
            st.markdown(final_state["final_report"])

            st.divider()

            st.subheader("Research Statistics")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Sources",
                len(final_state["sources"]),
            )

            col2.metric(
                "Extracted Facts",
                len(final_state["extracted_facts"]),
            )

            col3.metric(
                "Tool Calls",
                final_state["tool_call_count"],
            )

            with st.expander("View Sources"):
                for source in final_state["sources"]:
                    st.markdown(
                        f"- **{source['title']}** "
                        f"([Open source]({source['url']}))"
                    )

            st.download_button(
                label="Download Research Report",
                data=final_state["final_report"],
                file_name="research_report.md",
                mime="text/markdown",
            )


        except Exception as e:
            st.error(f"Research failed: {str(e)}")
