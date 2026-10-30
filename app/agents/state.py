from typing import TypedDict, List, Optional


class HealthcareState(TypedDict):
    """Shared state passed between all agents in the graph."""
    symptoms: str
    patient_info: Optional[str]
    research_output: Optional[str]
    plan_output: Optional[str]
    schedule_output: Optional[str]
    summary_output: Optional[str]
    final_response: Optional[str]
    messages: List[str]
