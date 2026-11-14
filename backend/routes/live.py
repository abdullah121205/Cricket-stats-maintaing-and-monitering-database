from flask import Blueprint, request, jsonify
from backend.db import Database
from api.cricket_api import cricket_api

live_bp = Blueprint("live", __name__, url_prefix="/api/live")

@live_bp.route("/scores", methods=["GET"])
def get_live_scores():
    """Returns current live international cricket scores."""
    try:
        result = cricket_api.get_live_scores()
        return jsonify({
            "success": True,
            "source": result.get("source"),
            "data": result.get("data", []),
            "has_api_key": result.get("has_api_key", False),
            "message": result.get("message", "Live scores retrieved")
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Error fetching live scores: {e}"}), 500

@live_bp.route("/scores/<match_id>", methods=["GET"])
def get_single_live_score(match_id):
    """Returns single live match details by match ID."""
    result = cricket_api.get_live_scores()
    matches = result.get("data", [])
    found = next((m for m in matches if str(m.get("id")) == str(match_id)), None)
    if not found:
        return jsonify({"success": False, "message": "Live match not found"}), 404
    return jsonify({"success": True, "data": found})

@live_bp.route("/import", methods=["POST"])
def import_live_match():
    """Imports or syncs a live match directly into the local database."""
    data = request.json or {}
    match_data = data.get("match") or data
    if not match_data or not match_data.get("title"):
        return jsonify({"success": False, "message": "Valid match data required"}), 400

    try:
        import_res = cricket_api.import_live_match(match_data, Database)
        action_verb = "imported as a new tracked match" if import_res.get("is_new") else "updated in database"
        return jsonify({
            "success": True,
            "message": f"Match successfully {action_verb}!",
            "match_id": import_res.get("match_id"),
            "is_new": import_res.get("is_new")
        }), 201 if import_res.get("is_new") else 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to import match: {e}"}), 500
