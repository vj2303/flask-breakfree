# application/routes/llmwork.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from application.controllers.llm_competency import generate_competency_report
from application.controllers.llm_summary import generate_summary


@LLM.route("/api/competency-report", methods=["POST"])
def api_competency_report():
    """
    Body:
    {
      "input_context": {... or [...]},  # your per-competency data block
      "candidate_name": "Alice"
    }
    Returns JSON report.
    """
    payload = request.get_json(silent=True) or {}
    input_context = payload.get("input_context")
    candidate_name = payload.get("candidate_name")

    if not input_context or not candidate_name:
        return jsonify({"error": "input_context and candidate_name are required"}), 400

    try:
        report = generate_competency_report(input_context, candidate_name)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@LLM.route("/api/summary", methods=["POST"])
def api_summary():
    """
    Body:
    {
      "summary_data": [{"competency": "...", "application_score": 3.2, ...}, ...],
      "candidate_first_name": "Alice"
    }
    Returns JSON summary.
    """
    payload = request.get_json(silent=True) or {}
    summary_data = payload.get("summary_data")
    candidate_first_name = payload.get("candidate_first_name")

    if not isinstance(summary_data, list) or not candidate_first_name:
        return jsonify({"error": "summary_data (list) and candidate_first_name are required"}), 400

    try:
        summary = generate_summary(summary_data, candidate_first_name)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
