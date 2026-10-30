from flask import Blueprint, request, jsonify
from app.agents.graph import run_healthcare_agents
import traceback

api_bp = Blueprint("api", __name__)


@api_bp.route("/analyze", methods=["POST"])
def analyze():
    """Main endpoint: runs all agents and returns structured results."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400

        symptoms = data.get("symptoms", "").strip()
        patient_info = data.get("patient_info", "").strip()

        if not symptoms:
            return jsonify({"error": "Symptoms field is required"}), 400

        if len(symptoms) < 5:
            return jsonify({"error": "Please describe your symptoms in more detail"}), 400

        result = run_healthcare_agents(symptoms=symptoms, patient_info=patient_info)

        return jsonify({
            "success": True,
            "data": {
                "research": result.get("research_output", ""),
                "plan": result.get("plan_output", ""),
                "schedule": result.get("schedule_output", ""),
                "summary": result.get("summary_output", ""),
                "agent_messages": result.get("messages", []),
            }
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Agent pipeline failed: {str(e)}"
        }), 500


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "Healthcare AI Microservice"})
