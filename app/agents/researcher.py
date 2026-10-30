from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.agents.state import HealthcareState
import os


RESEARCHER_PROMPT = PromptTemplate(
    input_variables=["symptoms", "patient_info"],
    template="""You are a Medical Research Agent specializing in symptom analysis and medical knowledge.

Patient Information: {patient_info}
Reported Symptoms: {symptoms}

Your task:
1. Analyze the reported symptoms thoroughly
2. Identify possible medical conditions (list top 3-5 possibilities)
3. Note any red-flag symptoms that require urgent attention
4. Provide relevant medical background for each condition
5. Suggest initial diagnostic considerations

Format your response with clear sections:
## Symptom Analysis
## Possible Conditions
## Red Flag Indicators
## Diagnostic Considerations

Be thorough but use clear, understandable language. Always recommend consulting a healthcare professional.
"""
)


def researcher_agent(state: HealthcareState) -> HealthcareState:
    """Research agent that analyzes symptoms and identifies possible conditions."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
    )

    chain = RESEARCHER_PROMPT | llm

    result = chain.invoke({
        "symptoms": state["symptoms"],
        "patient_info": state.get("patient_info", "Not provided"),
    })

    state["research_output"] = result.content
    state["messages"].append("✅ Researcher Agent: Symptom analysis complete")
    return state
