from flask import Blueprint, request, jsonify
from backend.db import Database

players_bp = Blueprint("players", __name__, url_prefix="/api/players")

@players_bp.route("", methods=["GET"])
def get_players():
    search = request.args.get("search", "").strip()
    role = request.args.get("role", "").strip()
    nationality = request.args.get("nationality", "").strip()

    sql = """
        SELECT p.*
        FROM players p
        WHERE 1=1
    """
    params = []

    if search:
        sql += " AND (p.full_name LIKE %s OR p.nationality LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if role:
        sql += " AND p.role = %s"
        params.append(role)

    if nationality:
        sql += " AND p.nationality = %s"
        params.append(nationality)

    sql += " ORDER BY p.full_name ASC"
    players = Database.query_all(sql, params)
    return jsonify({"success": True, "data": players, "count": len(players)})

@players_bp.route("/<int:player_id>", methods=["GET"])
def get_player(player_id):
    player = Database.query_one("SELECT * FROM players WHERE player_id = %s", (player_id,))
    if not player:
        return jsonify({"success": False, "message": "Player not found"}), 404

    # Career Batting
    batting = Database.query_one("""
        SELECT 
            COUNT(bs.batting_stat_id) AS innings,
            COALESCE(SUM(bs.runs), 0) AS total_runs,
            COALESCE(MAX(bs.runs), 0) AS highest_score,
            COALESCE(SUM(bs.balls_faced), 0) AS total_balls,
            COALESCE(SUM(bs.fours), 0) AS total_fours,
            COALESCE(SUM(bs.sixes), 0) AS total_sixes,
            ROUND(
                CASE 
                    WHEN SUM(bs.is_out) > 0 THEN SUM(bs.runs) * 1.0 / SUM(bs.is_out)
                    ELSE SUM(bs.runs) * 1.0
                END, 2
            ) AS batting_average,
            ROUND(
                CASE 
                    WHEN SUM(bs.balls_faced) > 0 THEN (SUM(bs.runs) * 100.0) / SUM(bs.balls_faced)
                    ELSE 0.00
                END, 2
            ) AS strike_rate,
            COALESCE(SUM(CASE WHEN bs.runs >= 50 AND bs.runs < 100 THEN 1 ELSE 0 END), 0) AS half_centuries,
            COALESCE(SUM(CASE WHEN bs.runs >= 100 THEN 1 ELSE 0 END), 0) AS centuries
        FROM batting_stats bs
        WHERE bs.player_id = %s
    """, (player_id,))

    # Career Bowling
    bowling = Database.query_one("""
        SELECT 
            COUNT(bw.bowling_stat_id) AS innings_bowled,
            COALESCE(SUM(bw.legal_balls), 0) AS total_balls,
            ROUND(COALESCE(SUM(bw.legal_balls), 0) / 6.0, 1) AS total_overs,
            COALESCE(SUM(bw.maidens), 0) AS total_maidens,
            COALESCE(SUM(bw.runs_conceded), 0) AS total_runs_conceded,
            COALESCE(SUM(bw.wickets), 0) AS total_wickets,
            ROUND(
                CASE 
                    WHEN SUM(bw.wickets) > 0 THEN SUM(bw.runs_conceded) * 1.0 / SUM(bw.wickets)
                    ELSE 0.00
                END, 2
            ) AS bowling_average,
            ROUND(
                CASE 
                    WHEN SUM(bw.legal_balls) > 0 THEN (SUM(bw.runs_conceded) * 6.0) / SUM(bw.legal_balls)
                    ELSE 0.00
                END, 2
            ) AS economy_rate,
            COALESCE(SUM(CASE WHEN bw.wickets >= 5 THEN 1 ELSE 0 END), 0) AS five_wicket_hauls
        FROM bowling_stats bw
        WHERE bw.player_id = %s
    """, (player_id,))

    # Recent Batting
    recent_batting = Database.query_all("""
        SELECT bs.*, m.match_title, m.format, m.match_date
        FROM batting_stats bs
        JOIN innings i ON bs.innings_id = i.innings_id
        JOIN matches m ON i.match_id = m.match_id
        WHERE bs.player_id = %s
        ORDER BY m.match_date DESC
        LIMIT 5
    """, (player_id,))

    # Recent Bowling
    recent_bowling = Database.query_all("""
        SELECT bw.*, m.match_title, m.format, m.match_date
        FROM bowling_stats bw
        JOIN innings i ON bw.innings_id = i.innings_id
        JOIN matches m ON i.match_id = m.match_id
        WHERE bw.player_id = %s
        ORDER BY m.match_date DESC
        LIMIT 5
    """, (player_id,))

    return jsonify({
        "success": True,
        "data": {
            "profile": player,
            "batting": batting,
            "bowling": bowling,
            "recent_batting": recent_batting,
            "recent_bowling": recent_bowling
        }
    })

@players_bp.route("", methods=["POST"])
def create_player():
    data = request.json or {}
    full_name = data.get("full_name") or data.get("name", "").strip()
    nationality = data.get("nationality") or data.get("country", "").strip()
    role = data.get("role", "Batter").strip()
    date_of_birth = data.get("date_of_birth") or data.get("dob")
    batting_style = data.get("batting_style", "Right-hand bat")
    bowling_style = data.get("bowling_style", "")

    if not full_name or not nationality or not role:
        return jsonify({"success": False, "message": "Full name, nationality, and role are required"}), 400

    new_id = Database.execute("""
        INSERT INTO players (full_name, nationality, role, date_of_birth, batting_style, bowling_style, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, 1)
    """, (full_name, nationality, role, date_of_birth, batting_style, bowling_style))

    return jsonify({"success": True, "message": "Player added successfully", "player_id": new_id}), 201

@players_bp.route("/<int:player_id>", methods=["PUT"])
def update_player(player_id):
    data = request.json or {}
    existing = Database.query_one("SELECT * FROM players WHERE player_id = %s", (player_id,))
    if not existing:
        return jsonify({"success": False, "message": "Player not found"}), 404

    full_name = data.get("full_name") or data.get("name", existing["full_name"])
    nationality = data.get("nationality") or data.get("country", existing["nationality"])
    role = data.get("role", existing["role"])
    date_of_birth = data.get("date_of_birth") or data.get("dob", existing["date_of_birth"])
    batting_style = data.get("batting_style", existing["batting_style"])
    bowling_style = data.get("bowling_style", existing["bowling_style"])

    Database.execute("""
        UPDATE players 
        SET full_name = %s, nationality = %s, role = %s, date_of_birth = %s, 
            batting_style = %s, bowling_style = %s
        WHERE player_id = %s
    """, (full_name, nationality, role, date_of_birth, batting_style, bowling_style, player_id))

    return jsonify({"success": True, "message": "Player updated successfully"})

@players_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    existing = Database.query_one("SELECT * FROM players WHERE player_id = %s", (player_id,))
    if not existing:
        return jsonify({"success": False, "message": "Player not found"}), 404

    Database.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
    return jsonify({"success": True, "message": "Player deleted successfully"})
