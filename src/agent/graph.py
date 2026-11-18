from langgraph.graph import StateGraph, START, END

from src.agent.state import ResearchState

from src.agent.nodes import (
    planner_node,
    search_node,
    reader_node,
    extractor_node,
    synthesis_node,
    report_node,
)

builder = StateGraph(ResearchState)

builder.add_node("planner", planner_node)
builder.add_node("search", search_node)
builder.add_node("reader", reader_node)
builder.add_node("extractor", extractor_node)
builder.add_node("synthesis", synthesis_node)
builder.add_node("report", report_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "search")
builder.add_edge("search", "reader")
builder.add_edge("reader", "extractor")
builder.add_edge("extractor", "synthesis")
builder.add_edge("synthesis", "report")
builder.add_edge("report", END)

graph = builder.compile()