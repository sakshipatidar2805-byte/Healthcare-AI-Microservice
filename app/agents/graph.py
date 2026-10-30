from langgraph.graph import StateGraph, END
from app.agents.state import HealthcareState
from app.agents.researcher import researcher_agent
from app.agents.planner import planner_agent
from app.agents.scheduler import scheduler_agent
from app.agents.summarizer import summarizer_agent


def build_healthcare_graph() -> StateGraph:
    """Build and compile the LangGraph agent workflow."""

    workflow = StateGraph(HealthcareState)

    # Add agent nodes
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("planner", planner_agent)
    workflow.add_node("scheduler", scheduler_agent)
    workflow.add_node("summarizer", summarizer_agent)

    # Define the sequential flow
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "planner")
    workflow.add_edge("planner", "scheduler")
    workflow.add_edge("scheduler", "summarizer")
    workflow.add_edge("summarizer", END)

    return workflow.compile()


# Singleton graph instance — rebuilt fresh on each server start
_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_healthcare_graph()
    return _graph


def run_healthcare_agents(symptoms: str, patient_info: str = "") -> dict:
    """
    Run the full multi-agent healthcare pipeline.

    Returns a dict with all agent outputs and status messages.
    """
    graph = get_graph()

    initial_state: HealthcareState = {
        "symptoms": symptoms,
        "patient_info": patient_info,
        "research_output": None,
        "plan_output": None,
        "schedule_output": None,
        "summary_output": None,
        "final_response": None,
        "messages": [],
    }

    result = graph.invoke(initial_state)
    return result
