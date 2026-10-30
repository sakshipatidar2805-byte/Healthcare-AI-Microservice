
import os
import streamlit as st
from dotenv import load_dotenv

from app.agents.graph import run_healthcare_agents


# Load environment variables from local .env file
load_dotenv()


# Streamlit page configuration
st.set_page_config(
    page_title="Healthcare AI Assistant",
    page_icon="🏥",
    layout="wide"
)


# Load API key from Streamlit Cloud Secrets or local .env
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key


# Application title
st.title("🏥 Healthcare AI Assistant")

st.write(
    "AI-powered healthcare research and assistance"
)


# Medical disclaimer
st.warning(
    "This tool provides AI-generated information, not a medical diagnosis. "
    "Always consult a qualified healthcare professional. "
    "For emergencies, seek immediate medical attention."
)


# Patient information form
st.subheader("Patient Information")

with st.form("healthcare_form"):

    symptoms = st.text_area(
        "Describe your symptoms *",
        placeholder="Example: Headache and fever for two days..."
    )

    patient_info = st.text_area(
        "Additional information (optional)",
        placeholder="Age or relevant general information. "
                    "Avoid names and personal identifiers."
    )

    submitted = st.form_submit_button(
        "Analyze Symptoms"
    )


# Process submitted information
if submitted:

    if not symptoms.strip():
        st.error("Please enter your symptoms.")

    elif len(symptoms.strip()) < 5:
        st.error("Please provide a more detailed description.")

    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("Google API key is not configured.")

    else:

        try:

            with st.spinner(
                "AI agents are analyzing your information..."
            ):

                result = run_healthcare_agents(
                    symptoms=symptoms.strip(),
                    patient_info=patient_info.strip()
                )

            st.success("Analysis completed!")

            # Section 1: Symptom Research
            st.subheader("1. Symptom Research")

            st.markdown(
                result.get("research_output")
                or "No output available."
            )

            # Section 2: Healthcare Plan
            st.subheader("2. Healthcare Plan")

            st.markdown(
                result.get("plan_output")
                or "No output available."
            )

            # Section 3: Schedule
            st.subheader("3. Schedule")

            st.markdown(
                result.get("schedule_output")
                or "No output available."
            )

            # Section 4: Final Summary
            st.subheader("4. Final Summary")

            st.markdown(
                result.get("summary_output")
                or "No output available."
            )

        except Exception as e:

            error_message = str(e).lower()

            # Handle Gemini API quota errors
            if (
                "resource_exhausted" in error_message
                or "resourceexhausted" in error_message
                or "429" in error_message
                or "quota" in error_message
            ):

                st.warning(
                    "Gemini API ki free daily request limit khatam ho gayi hai."
                )

                st.info(
                    "Google ke quota reset hone tak wait karein. "
                    "Uske baad dobara try karein."
                )

            else:

                st.error(
                    "Analysis failed. Please check the application configuration."
                )

                st.exception(e)
