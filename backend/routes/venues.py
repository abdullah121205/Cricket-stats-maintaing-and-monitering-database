from flask import Blueprint, request, jsonify
from backend.db import Database

venues_bp = Blueprint("venues", __name__, url_prefix="/api/venues")

@venues_bp.route("", methods=["GET"])
def get_venues():
    venues = Database.query_all("SELECT * FROM venues ORDER BY venue_name ASC")
    return jsonify({"success": True, "data": venues, "count": len(venues)})

@venues_bp.route("", methods=["POST"])
def create_venue():
    data = request.json or {}
    name = data.get("venue_name") or data.get("name", "").strip()
    city = data.get("city", "").strip()
    country = data.get("country", "").strip()

    if not name:
        return jsonify({"success": False, "message": "Venue name is required"}), 400

    new_id = Database.execute("""
        INSERT INTO venues (venue_name, city, country)
        VALUES (%s, %s, %s)
    """, (name, city, country))

    return jsonify({"success": True, "message": "Venue created", "venue_id": new_id}), 201
