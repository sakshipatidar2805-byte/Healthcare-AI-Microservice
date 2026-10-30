from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.agents.state import HealthcareState
import os


PLANNER_PROMPT = PromptTemplate(
    input_variables=["symptoms", "research_output"],
    template="""You are a Medical Treatment Planning Agent. Based on the research findings, create a comprehensive care plan.

Original Symptoms: {symptoms}

Research Findings:
{research_output}

Your task — create a structured treatment plan:
1. Immediate actions the patient should take
2. Recommended lifestyle modifications
3. Dietary recommendations
4. Medications to consider (OTC only; always advise consulting a doctor for prescriptions)
5. Home remedies and supportive care
6. When to seek emergency care

Format your response with clear sections:
## Immediate Actions
## Treatment Recommendations
## Lifestyle & Diet Changes
## Home Care Tips
## Warning Signs — Seek Emergency Care

Keep recommendations practical, safe, and evidence-based. Always emphasize professional medical consultation.
"""
)


def planner_agent(state: HealthcareState) -> HealthcareState:
    """Planner agent that creates a treatment and care plan."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.4,
    )

    chain = PLANNER_PROMPT | llm

    result = chain.invoke({
        "symptoms": state["symptoms"],
        "research_output": state.get("research_output", ""),
    })

    state["plan_output"] = result.content
    state["messages"].append("✅ Planner Agent: Treatment plan created")
    return state
