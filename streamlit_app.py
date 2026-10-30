
import os
import streamlit as st
from dotenv import load_dotenv
from app.agents.graph import run_healthcare_agents

load_dotenv()

# Streamlit Cloud secrets
# Load API key from Streamlit Cloud secrets or local .env
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

st.set_page_config(
    page_title="Healthcare AI Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare AI Assistant")
st.write("AI-powered healthcare research and assistance")

st.warning(
    "This tool provides AI-generated information, not a medical diagnosis. "
    "Always consult a qualified healthcare professional. "
    "For emergencies, seek immediate medical attention."
)

st.subheader("Patient Information")

with st.form("healthcare_form"):
    symptoms = st.text_area(
        "Describe your symptoms *",
        placeholder="Example: Headache and fever for two days..."
    )

    patient_info = st.text_area(
        "Additional information (optional)",
        placeholder="Age or relevant general information. Avoid names and personal identifiers."
    )

    submitted = st.form_submit_button("Analyze Symptoms")

if submitted:
    if not symptoms.strip():
        st.error("Please enter your symptoms.")
    elif len(symptoms.strip()) < 5:
        st.error("Please provide a more detailed description.")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("Google API key is not configured.")
    else:
        try:
            with st.spinner("AI agents are analyzing your information..."):
                result = run_healthcare_agents(
                    symptoms=symptoms.strip(),
                    patient_info=patient_info.strip()
                )

            st.success("Analysis completed!")

            st.subheader("1. Symptom Research")
            st.markdown(result.get("research_output") or "No output available.")

            st.subheader("2. Healthcare Plan")
            st.markdown(result.get("plan_output") or "No output available.")

            st.subheader("3. Schedule")
            st.markdown(result.get("schedule_output") or "No output available.")

            st.subheader("4. Final Summary")
            st.markdown(result.get("summary_output") or "No output available.")

        except Exception as e:
            st.error("Analysis failed. Please check the application configuration.")
            st.exception(e)
