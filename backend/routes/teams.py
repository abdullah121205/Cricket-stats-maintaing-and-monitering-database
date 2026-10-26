from flask import Blueprint, request, jsonify
from backend.db import Database

teams_bp = Blueprint("teams", __name__, url_prefix="/api/teams")

@teams_bp.route("", methods=["GET"])
def get_teams():
    sql = """
        SELECT 
            t.team_id,
            t.team_name,
            t.country,
            t.team_type,
            COUNT(DISTINCT m.match_id) AS matches_played,
            SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS wins,
            SUM(CASE WHEN m.winner_team_id IS NOT NULL AND m.winner_team_id <> t.team_id THEN 1 ELSE 0 END) AS losses,
            ROUND(
                SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(DISTINCT m.match_id), 0), 1
            ) AS win_percentage,
            (SELECT COUNT(*) FROM players p WHERE p.nationality = t.country) AS squad_count
        FROM teams t
        LEFT JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id) AND m.status = 'Completed'
        GROUP BY t.team_id, t.team_name, t.country, t.team_type
        ORDER BY wins DESC, t.team_name ASC
    """
    teams = Database.query_all(sql)
    return jsonify({"success": True, "data": teams, "count": len(teams)})

@teams_bp.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):
    team = Database.query_one("SELECT * FROM teams WHERE team_id = %s", (team_id,))
    if not team:
        return jsonify({"success": False, "message": "Team not found"}), 404

    # Squad based on nationality or match_players
    squad = Database.query_all("""
        SELECT player_id, full_name, nationality, role, batting_style, bowling_style
        FROM players
        WHERE nationality = %s
        ORDER BY role, full_name
    """, (team["country"],))

    matches = Database.query_all("""
        SELECT m.*, t1.team_name AS team1_name, t2.team_name AS team2_name, w.team_name AS winner_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams w ON m.winner_team_id = w.team_id
        WHERE m.team1_id = %s OR m.team2_id = %s
        ORDER BY m.match_date DESC
    """, (team_id, team_id))

    return jsonify({
        "success": True,
        "data": {
            "team": team,
            "squad": squad,
            "matches": matches
        }
    })

@teams_bp.route("", methods=["POST"])
def create_team():
    data = request.json or {}
    team_name = data.get("team_name") or data.get("name", "").strip()
    country = data.get("country", "").strip()
    team_type = data.get("team_type", "International")

    if not team_name:
        return jsonify({"success": False, "message": "Team name is required"}), 400

    new_id = Database.execute("""
        INSERT INTO teams (team_name, country, team_type)
        VALUES (%s, %s, %s)
    """, (team_name, country, team_type))

    return jsonify({"success": True, "message": "Team created successfully", "team_id": new_id}), 201

@teams_bp.route("/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    existing = Database.query_one("SELECT * FROM teams WHERE team_id = %s", (team_id,))
    if not existing:
        return jsonify({"success": False, "message": "Team not found"}), 404

    Database.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
    return jsonify({"success": True, "message": "Team deleted successfully"})
