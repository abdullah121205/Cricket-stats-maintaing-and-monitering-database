from flask import Blueprint, jsonify
from backend.db import Database

stats_bp = Blueprint("stats", __name__, url_prefix="/api/stats")

@stats_bp.route("/summary", methods=["GET"])
def get_summary():
    total_players = Database.query_one("SELECT COUNT(*) AS count FROM players")["count"]
    total_teams = Database.query_one("SELECT COUNT(*) AS count FROM teams")["count"]
    total_matches = Database.query_one("SELECT COUNT(*) AS count FROM matches")["count"]
    completed_matches = Database.query_one("SELECT COUNT(*) AS count FROM matches WHERE status = 'Completed'")["count"]
    
    batting_totals = Database.query_one("""
        SELECT COALESCE(SUM(runs), 0) AS total_runs, 
               COALESCE(SUM(fours), 0) AS total_fours, 
               COALESCE(SUM(sixes), 0) AS total_sixes 
        FROM batting_stats
    """)
    
    bowling_totals = Database.query_one("""
        SELECT COALESCE(SUM(wickets), 0) AS total_wickets,
               COALESCE(SUM(maidens), 0) AS total_maidens
        FROM bowling_stats
    """)

    return jsonify({
        "success": True,
        "data": {
            "total_players": total_players,
            "total_teams": total_teams,
            "total_matches": total_matches,
            "completed_matches": completed_matches,
            "total_runs": batting_totals["total_runs"],
            "total_fours": batting_totals["total_fours"],
            "total_sixes": batting_totals["total_sixes"],
            "total_wickets": bowling_totals["total_wickets"],
            "total_maidens": bowling_totals["total_maidens"]
        }
    })

@stats_bp.route("/top-batsmen", methods=["GET"])
def get_top_batsmen():
    sql = """
        SELECT 
            p.player_id,
            p.full_name AS player_name,
            p.nationality AS country,
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
        FROM players p
        JOIN batting_stats bs ON p.player_id = bs.player_id
        GROUP BY p.player_id, p.full_name, p.nationality
        ORDER BY total_runs DESC
        LIMIT 10
    """
    data = Database.query_all(sql)
    return jsonify({"success": True, "data": data})

@stats_bp.route("/top-bowlers", methods=["GET"])
def get_top_bowlers():
    sql = """
        SELECT 
            p.player_id,
            p.full_name AS player_name,
            p.nationality AS country,
            COUNT(bw.bowling_stat_id) AS innings_bowled,
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
        FROM players p
        JOIN bowling_stats bw ON p.player_id = bw.player_id
        GROUP BY p.player_id, p.full_name, p.nationality
        ORDER BY total_wickets DESC, economy_rate ASC
        LIMIT 10
    """
    data = Database.query_all(sql)
    return jsonify({"success": True, "data": data})

@stats_bp.route("/highest-scores", methods=["GET"])
def get_highest_scores():
    sql = """
        SELECT 
            bs.batting_stat_id,
            p.player_id,
            p.full_name AS player_name,
            p.nationality AS country,
            bs.runs,
            bs.balls_faced AS balls,
            bs.fours,
            bs.sixes,
            ROUND(bs.runs * 100.0 / NULLIF(bs.balls_faced, 0), 2) AS strike_rate,
            m.match_id,
            m.match_title,
            m.format AS match_format,
            m.match_date,
            v.venue_name
        FROM batting_stats bs
        JOIN players p ON bs.player_id = p.player_id
        JOIN innings i ON bs.innings_id = i.innings_id
        JOIN matches m ON i.match_id = m.match_id
        LEFT JOIN venues v ON m.venue_id = v.venue_id
        ORDER BY bs.runs DESC
        LIMIT 10
    """
    data = Database.query_all(sql)
    return jsonify({"success": True, "data": data})

@stats_bp.route("/top-strike-rates", methods=["GET"])
def get_top_strike_rates():
    sql = """
        SELECT 
            p.player_id,
            p.full_name AS player_name,
            p.nationality AS country,
            SUM(bs.runs) AS total_runs,
            SUM(bs.balls_faced) AS balls_faced,
            ROUND((SUM(bs.runs) * 100.0) / SUM(bs.balls_faced), 2) AS strike_rate
        FROM players p
        JOIN batting_stats bs ON p.player_id = bs.player_id
        GROUP BY p.player_id, p.full_name, p.nationality
        HAVING balls_faced >= 20
        ORDER BY strike_rate DESC
        LIMIT 10
    """
    data = Database.query_all(sql)
    return jsonify({"success": True, "data": data})

@stats_bp.route("/team-rankings", methods=["GET"])
def get_team_rankings():
    sql = """
        SELECT 
            t.team_id,
            t.team_name,
            t.country,
            COUNT(DISTINCT m.match_id) AS matches_played,
            SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS wins,
            SUM(CASE WHEN m.winner_team_id IS NOT NULL AND m.winner_team_id <> t.team_id THEN 1 ELSE 0 END) AS losses,
            ROUND(
                SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(DISTINCT m.match_id), 0), 1
            ) AS win_percentage
        FROM teams t
        LEFT JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id) AND m.status = 'Completed'
        GROUP BY t.team_id, t.team_name, t.country
        ORDER BY wins DESC, win_percentage DESC, t.team_name ASC
    """
    data = Database.query_all(sql)
    return jsonify({"success": True, "data": data})
