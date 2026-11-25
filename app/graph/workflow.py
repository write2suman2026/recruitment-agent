from langgraph.graph import StateGraph

from models.schema import AgentState

from agents.resume_agent import resume_agent
from agents.bias_agent import bias_agent
from agents.jd_extraction_agent import  jd_agent
from agents.matching_agent import matching_agent
from agents.explainability_agent import explain_agent


def build_graph():

    graph=StateGraph(AgentState)

    graph.add_node(
        "resume",
        resume_agent
    )

    graph.add_node(
        "bias",
        bias_agent
    )

    graph.add_node(
        "jd",
        jd_agent
    )

    graph.add_node(
        "match",
        matching_agent
    )

    graph.add_node(
        "explain",
        explain_agent
    )

    graph.set_entry_point("resume")

    graph.add_edge("resume","bias")
    graph.add_edge("bias","jd")
    graph.add_edge("jd","match")
    graph.add_edge("match","explain")

    return graph.compile()