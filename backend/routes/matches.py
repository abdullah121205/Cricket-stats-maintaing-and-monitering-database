from flask import Blueprint, request, jsonify
from backend.db import Database

matches_bp = Blueprint("matches", __name__, url_prefix="/api/matches")

@matches_bp.route("", methods=["GET"])
def get_matches():
    fmt = request.args.get("format", "").strip()
    status = request.args.get("status", "").strip()
    team_id = request.args.get("team_id", "").strip()

    sql = """
        SELECT m.*, 
               t1.team_name AS team1_name,
               t2.team_name AS team2_name,
               w.team_name AS winner_name,
               v.venue_name, v.city AS venue_city,
               pom.full_name AS player_of_match_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams w ON m.winner_team_id = w.team_id
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        LEFT JOIN players pom ON m.player_of_match_id = pom.player_id
        WHERE 1=1
    """
    params = []

    if fmt:
        sql += " AND m.format = %s"
        params.append(fmt)

    if status:
        sql += " AND m.status = %s"
        params.append(status)

    if team_id:
        sql += " AND (m.team1_id = %s OR m.team2_id = %s)"
        params.extend([team_id, team_id])

    sql += " ORDER BY m.match_date DESC, m.match_id DESC"
    matches = Database.query_all(sql, params)
    return jsonify({"success": True, "data": matches, "count": len(matches)})

@matches_bp.route("/<int:match_id>", methods=["GET"])
def get_match(match_id):
    sql = """
        SELECT m.*, 
               t1.team_name AS team1_name,
               t2.team_name AS team2_name,
               w.team_name AS winner_name,
               v.venue_name, v.city AS venue_city, v.country AS venue_country,
               pom.full_name AS player_of_match_name
        FROM matches m
        JOIN teams t1 ON m.team1_id = t1.team_id
        JOIN teams t2 ON m.team2_id = t2.team_id
        LEFT JOIN teams w ON m.winner_team_id = w.team_id
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        LEFT JOIN players pom ON m.player_of_match_id = pom.player_id
        WHERE m.match_id = %s
    """
    match = Database.query_one(sql, (match_id,))
    if not match:
        return jsonify({"success": False, "message": "Match not found"}), 404

    # Batting entries
    batting = Database.query_all("""
        SELECT bs.*, p.full_name AS player_name, bt.team_name AS batting_team_name,
               ROUND(bs.runs * 100.0 / NULLIF(bs.balls_faced, 0), 2) AS strike_rate
        FROM batting_stats bs
        JOIN innings i ON bs.innings_id = i.innings_id
        JOIN teams bt ON i.batting_team_id = bt.team_id
        JOIN players p ON bs.player_id = p.player_id
        WHERE i.match_id = %s
        ORDER BY i.innings_number ASC, bs.batting_position ASC, bs.runs DESC
    """, (match_id,))

    # Bowling entries
    bowling = Database.query_all("""
        SELECT bw.*, p.full_name AS player_name,
               ROUND(bw.legal_balls / 6.0, 1) AS overs,
               ROUND(bw.runs_conceded * 6.0 / NULLIF(bw.legal_balls, 0), 2) AS economy_rate
        FROM bowling_stats bw
        JOIN innings i ON bw.innings_id = i.innings_id
        JOIN players p ON bw.player_id = p.player_id
        WHERE i.match_id = %s
        ORDER BY i.innings_number ASC, bw.wickets DESC, bw.runs_conceded ASC
    """, (match_id,))

    return jsonify({
        "success": True,
        "data": {
            "match": match,
            "batting": batting,
            "bowling": bowling
        }
    })

@matches_bp.route("", methods=["POST"])
def create_match():
    data = request.json or {}
    match_title = data.get("match_title") or f"{data.get('team1_name', 'Team 1')} vs {data.get('team2_name', 'Team 2')}"
    fmt = data.get("format", "T20")
    match_date = data.get("match_date")
    venue_id = data.get("venue_id")
    team1_id = data.get("team1_id")
    team2_id = data.get("team2_id")
    status = data.get("status", "Scheduled")
    winner_team_id = data.get("winner_team_id")
    result_summary = data.get("result_summary") or data.get("result", "")

    if not match_date or not team1_id or not team2_id:
        return jsonify({"success": False, "message": "Date, team1, and team2 are required"}), 400

    match_id = Database.execute("""
        INSERT INTO matches (match_title, format, match_date, venue_id, team1_id, team2_id, status, winner_team_id, result_summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (match_title, fmt, match_date, venue_id, team1_id, team2_id, status, winner_team_id, result_summary))

    return jsonify({"success": True, "message": "Match created", "match_id": match_id}), 201

@matches_bp.route("/<int:match_id>/batting", methods=["POST"])
def add_batting_score(match_id):
    data = request.json or {}
    player_id = data.get("player_id")
    team_id = data.get("team_id")
    runs = int(data.get("runs", 0))
    balls_faced = int(data.get("balls_faced") or data.get("balls", 0))
    fours = int(data.get("fours", 0))
    sixes = int(data.get("sixes", 0))
    is_out = 1 if data.get("is_out", False) else 0
    dismissal_kind = data.get("dismissal_kind") or data.get("dismissal_type", "not out")

    # Find or create innings record
    inn = Database.query_one("SELECT innings_id FROM innings WHERE match_id = %s AND batting_team_id = %s", (match_id, team_id))
    if not inn:
        count_inn = Database.query_one("SELECT COUNT(*) AS c FROM innings WHERE match_id = %s", (match_id,))["c"] + 1
        inn_id = Database.execute("""
            INSERT INTO innings (match_id, innings_number, batting_team_id)
            VALUES (%s, %s, %s)
        """, (match_id, count_inn, team_id))
    else:
        inn_id = inn["innings_id"]

    stat_id = Database.execute("""
        INSERT INTO batting_stats (innings_id, player_id, runs, balls_faced, fours, sixes, is_out, dismissal_kind)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (inn_id, player_id, runs, balls_faced, fours, sixes, is_out, dismissal_kind))

    return jsonify({"success": True, "message": "Batting recorded", "batting_stat_id": stat_id}), 201

@matches_bp.route("/<int:match_id>/bowling", methods=["POST"])
def add_bowling_score(match_id):
    data = request.json or {}
    player_id = data.get("player_id")
    team_id = data.get("team_id")
    overs = float(data.get("overs", 0.0))
    legal_balls = int(data.get("legal_balls", int(overs) * 6 + int(round((overs % 1) * 10))))
    maidens = int(data.get("maidens", 0))
    runs_conceded = int(data.get("runs_conceded", 0))
    wickets = int(data.get("wickets", 0))

    # Opponent team is batting
    match = Database.query_one("SELECT team1_id, team2_id FROM matches WHERE match_id = %s", (match_id,))
    opp_team_id = match["team2_id"] if str(match["team1_id"]) == str(team_id) else match["team1_id"]

    inn = Database.query_one("SELECT innings_id FROM innings WHERE match_id = %s AND batting_team_id = %s", (match_id, opp_team_id))
    if not inn:
        count_inn = Database.query_one("SELECT COUNT(*) AS c FROM innings WHERE match_id = %s", (match_id,))["c"] + 1
        inn_id = Database.execute("""
            INSERT INTO innings (match_id, innings_number, batting_team_id)
            VALUES (%s, %s, %s)
        """, (match_id, count_inn, opp_team_id))
    else:
        inn_id = inn["innings_id"]

    stat_id = Database.execute("""
        INSERT INTO bowling_stats (innings_id, player_id, legal_balls, maidens, runs_conceded, wickets)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (inn_id, player_id, legal_balls, maidens, runs_conceded, wickets))

    return jsonify({"success": True, "message": "Bowling recorded", "bowling_stat_id": stat_id}), 201

@matches_bp.route("/<int:match_id>", methods=["DELETE"])
def delete_match(match_id):
    existing = Database.query_one("SELECT * FROM matches WHERE match_id = %s", (match_id,))
    if not existing:
        return jsonify({"success": False, "message": "Match not found"}), 404

    Database.execute("DELETE FROM matches WHERE match_id = %s", (match_id,))
    return jsonify({"success": True, "message": "Match deleted successfully"})
