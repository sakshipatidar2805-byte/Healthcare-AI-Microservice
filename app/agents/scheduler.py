from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.agents.state import HealthcareState
import os


SCHEDULER_PROMPT = PromptTemplate(
    input_variables=["symptoms", "plan_output"],
    template="""You are a Healthcare Scheduling Agent. Create a practical follow-up schedule and appointment plan.

Patient Symptoms: {symptoms}

Treatment Plan:
{plan_output}

Your task — create a detailed healthcare schedule:
1. Immediate (Today / Next 24 hours): What to do right now
2. Short-term (Days 1–7): Daily care routine
3. Medium-term (Week 2–4): Follow-up actions
4. Long-term (Month 1–3): Ongoing monitoring
5. Specialist referrals needed (which type of doctor to see)
6. Tests and investigations recommended

Format your response with clear sections:
## Immediate Schedule (Today)
## Week 1 Plan
## Month 1 Follow-up
## Specialist Referrals
## Recommended Tests & Investigations
## Monitoring Checklist

Make the schedule realistic and actionable. Include specific timeframes.
"""
)


def scheduler_agent(state: HealthcareState) -> HealthcareState:
    """Scheduler agent that creates a follow-up and appointment schedule."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )

    chain = SCHEDULER_PROMPT | llm

    result = chain.invoke({
        "symptoms": state["symptoms"],
        "plan_output": state.get("plan_output", ""),
    })

    state["schedule_output"] = result.content
    state["messages"].append("✅ Scheduler Agent: Follow-up schedule created")
    return state
