from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.agents.state import HealthcareState
import os


SUMMARIZER_PROMPT = PromptTemplate(
    input_variables=["symptoms", "patient_info", "research_output", "plan_output", "schedule_output"],
    template="""You are a Medical Summary Agent. Compile all findings into a clear, structured patient summary report.

Patient Information: {patient_info}
Reported Symptoms: {symptoms}

Research Findings:
{research_output}

Treatment Plan:
{plan_output}

Follow-up Schedule:
{schedule_output}

Create a comprehensive Patient Summary Report with:
1. Executive summary (2-3 sentences)
2. Key findings
3. Priority actions (numbered, most urgent first)
4. Complete care plan overview
5. Important disclaimers

Format as a professional medical summary. Use clear headings and bullet points.
Start with: "📋 PATIENT HEALTH SUMMARY REPORT"

End with a clear disclaimer that this is AI-generated guidance and not a substitute for professional medical advice.
"""
)


def summarizer_agent(state: HealthcareState) -> HealthcareState:
    """Summarizer agent that compiles all outputs into a final patient report."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
    )

    chain = SUMMARIZER_PROMPT | llm

    result = chain.invoke({
        "symptoms": state["symptoms"],
        "patient_info": state.get("patient_info", "Not provided"),
        "research_output": state.get("research_output", ""),
        "plan_output": state.get("plan_output", ""),
        "schedule_output": state.get("schedule_output", ""),
    })

    state["summary_output"] = result.content
    state["final_response"] = result.content
    state["messages"].append("✅ Summarizer Agent: Patient summary report generated")
    return state
