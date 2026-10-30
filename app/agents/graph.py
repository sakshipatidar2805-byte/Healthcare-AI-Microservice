from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.agents.state import HealthcareState
import os


HEALTHCARE_PROMPT = PromptTemplate(
    input_variables=["symptoms", "patient_info"],
    template="""You are a Healthcare AI Assistant.

Analyze the patient's information and generate all four sections.

Patient Information: {patient_info}
Symptoms: {symptoms}

Return exactly these four sections:

## RESEARCH_OUTPUT
Analyze symptoms, list possible conditions, red flags and diagnostic considerations.
Do not claim a confirmed diagnosis.

## PLAN_OUTPUT
Provide safe general care guidance, lifestyle and dietary suggestions.
Do not prescribe medication or dosages.
Recommend professional medical consultation.

## SCHEDULE_OUTPUT
Provide a practical follow-up schedule, specialist referrals and possible tests to discuss with a doctor.
Do not present tests as mandatory.

## SUMMARY_OUTPUT
Provide an executive summary, key findings, priority actions and disclaimers.

Important:
- This is informational guidance, not a medical diagnosis.
- Clearly identify emergency warning signs.
- For emergencies, advise immediate medical attention.
- Never invent medical certainty.
- Use clear, understandable language.
"""
)


def combined_healthcare_agent(state: HealthcareState) -> HealthcareState:
    """Generate all four healthcare outputs using one Gemini request."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )

    chain = HEALTHCARE_PROMPT | llm

    result = chain.invoke({
        "symptoms": state["symptoms"],
        "patient_info": state.get("patient_info") or "Not provided",
    })

    response = result.content

    sections = {
        "research_output": "## RESEARCH_OUTPUT",
        "plan_output": "## PLAN_OUTPUT",
        "schedule_output": "## SCHEDULE_OUTPUT",
        "summary_output": "## SUMMARY_OUTPUT",
    }

    positions = {
        key: response.find(marker)
        for key, marker in sections.items()
    }

    if any(position == -1 for position in positions.values()):
        raise ValueError("Gemini response is missing one or more required sections.")

    ordered = sorted(positions.items(), key=lambda item: item[1])

    for index, (key, start) in enumerate(ordered):
        content_start = start + len(sections[key])
        content_end = (
            ordered[index + 1][1]
            if index + 1 < len(ordered)
            else len(response)
        )
        state[key] = response[content_start:content_end].strip()

    state["final_response"] = state["summary_output"]
    state["messages"].append(
        "Healthcare analysis completed using one Gemini API request."
    )

    return state


def build_healthcare_graph():
    """Build the optimized single-call healthcare workflow."""

    workflow = StateGraph(HealthcareState)

    workflow.add_node("healthcare_analysis", combined_healthcare_agent)

    workflow.set_entry_point("healthcare_analysis")
    workflow.add_edge("healthcare_analysis", END)

    return workflow.compile()


_graph = None


def get_graph():
    global _graph

    if _graph is None:
        _graph = build_healthcare_graph()

    return _graph


def run_healthcare_agents(symptoms: str, patient_info: str = "") -> dict:

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

    return get_graph().invoke(initial_state)