"""
Cricket External & Live API Integration Service
Provides real-time scores, CricAPI synchronization, dynamic live match simulation,
and one-click import into the local relational database.
"""

import os
import json
import time
from datetime import datetime, date
from urllib.request import Request, urlopen
from urllib.error import URLError

class CricketAPIClient:
    def __init__(self, api_key=None, base_url="https://api.cricapi.com/v1"):
        self.api_key = api_key or os.getenv("CRICKET_API_KEY", "").strip()
        self.base_url = base_url

    def get_live_scores(self):
        """
        Fetches live international cricket matches.
        Uses CricAPI if CRICKET_API_KEY is configured; otherwise provides
        a dynamic, high-fidelity real-time simulation engine.
        """
        if self.api_key:
            external_data = self._fetch_from_cricapi()
            if external_data and external_data.get("status") == "success":
                return {
                    "source": "cricapi",
                    "status": "success",
                    "count": len(external_data.get("data", [])),
                    "data": self._normalize_cricapi_matches(external_data.get("data", []))
                }

        # Dynamic simulation fallback with realistic live progression
        return {
            "source": "live_engine",
            "status": "success",
            "message": "Live feed active (Dynamic Real-Time Simulation)",
            "has_api_key": bool(self.api_key),
            "data": self._generate_simulated_live_matches()
        }

    def _fetch_from_cricapi(self):
        url = f"{self.base_url}/currentMatches?apikey={self.api_key}"
        try:
            req = Request(url, headers={"User-Agent": "CricketStatsDatabase/1.0"})
            with urlopen(req, timeout=8) as response:
                return json.loads(response.read().decode())
        except (URLError, Exception) as e:
            print(f"[CricketAPI Warning] External fetch failed: {e}")
            return None

    def _normalize_cricapi_matches(self, matches):
        normalized = []
        for m in matches:
            teams = m.get("teams", ["Team A", "Team B"])
            t1_name = teams[0] if len(teams) > 0 else "Team 1"
            t2_name = teams[1] if len(teams) > 1 else "Team 2"
            
            score_entries = m.get("score", [])
            t1_score = score_entries[0] if len(score_entries) > 0 else {}
            t2_score = score_entries[1] if len(score_entries) > 1 else {}

            normalized.append({
                "id": m.get("id"),
                "title": m.get("name") or f"{t1_name} vs {t2_name}",
                "format": (m.get("matchType") or "T20").upper(),
                "status": m.get("status", "Live"),
                "is_live": "won" not in m.get("status", "").lower(),
                "venue": m.get("venue", "International Cricket Ground"),
                "date": m.get("date", str(date.today())),
                "team1": {
                    "name": t1_name,
                    "runs": t1_score.get("r", 0),
                    "wickets": t1_score.get("w", 0),
                    "overs": t1_score.get("o", 0.0)
                },
                "team2": {
                    "name": t2_name,
                    "runs": t2_score.get("r", 0),
                    "wickets": t2_score.get("w", 0),
                    "overs": t2_score.get("o", 0.0)
                },
                "summary": m.get("status", ""),
                "current_batters": [],
                "current_bowler": None
            })
        return normalized

    def _generate_simulated_live_matches(self):
        """
        Generates realistic, time-evolving international matches.
        Scores subtly advance based on current clock seconds to simulate live balls being bowled.
        """
        now = int(time.time())
        # Cycle through match states every 600 seconds
        tick = (now // 15) % 40  # Advances every 15 seconds, up to 40 steps

        # Match 1: India vs Australia - 2nd ODI at Eden Gardens
        # Chase situation: Australia posted 287/8 in 50 overs. India chasing 288.
        ind_base_runs = 210 + (tick * 2)
        ind_balls = min(300, 206 + tick)
        ind_overs = f"{ind_balls // 6}.{ind_balls % 6}"
        ind_wkts = 3 if tick < 25 else 4
        ind_runs_needed = max(0, 288 - ind_base_runs)
        balls_left = max(0, 300 - ind_balls)
        crr = round((ind_base_runs * 6.0) / max(1, ind_balls), 2)
        rrr = round((ind_runs_needed * 6.0) / max(1, balls_left), 2) if balls_left > 0 else 0.0

        kohli_runs = 78 + (tick // 2)
        kohli_balls = 72 + (tick // 2)
        hardik_runs = 24 + ((tick * 3) // 2)
        hardik_balls = 18 + tick

        match_1_status = f"India need {ind_runs_needed} runs in {balls_left} balls" if ind_runs_needed > 0 else "India won by 6 wickets"

        # Match 2: England vs South Africa - 3rd T20I at The Oval
        # South Africa chasing England's 182/6
        sa_balls = min(120, 92 + tick)
        sa_overs = f"{sa_balls // 6}.{sa_balls % 6}"
        sa_base_runs = 142 + (tick * 2)
        sa_wkts = 4 if tick < 18 else 5
        sa_needed = max(0, 183 - sa_base_runs)
        sa_balls_left = max(0, 120 - sa_balls)
        sa_crr = round((sa_base_runs * 6.0) / max(1, sa_balls), 2)
        sa_rrr = round((sa_needed * 6.0) / max(1, sa_balls_left), 2) if sa_balls_left > 0 else 0.0

        klaasen_runs = 44 + tick
        klaasen_balls = 21 + (tick // 2)

        match_2_status = f"South Africa need {sa_needed} runs in {sa_balls_left} balls" if sa_needed > 0 else "South Africa won by 5 wickets"

        # Match 3: New Zealand vs Pakistan - 1st Test at Basin Reserve
        # Day 4: Pakistan 240 & 168/5 vs New Zealand 384
        pak_balls = 348 + tick
        pak_overs = f"{pak_balls // 6}.{pak_balls % 6}"
        pak_runs = 168 + tick
        trail = max(0, 384 - (240 + pak_runs))
        lead_trail_text = f"Pakistan trail by {trail} runs" if trail > 0 else f"Pakistan lead by {-trail} runs"

        return [
            {
                "id": "live_ind_aus_odi",
                "title": "India vs Australia - 2nd ODI",
                "series": "Australia Tour of India 2026",
                "format": "ODI",
                "status": "LIVE",
                "is_live": True,
                "venue": "Eden Gardens, Kolkata",
                "date": str(date.today()),
                "team1": {
                    "name": "India",
                    "short": "IND",
                    "runs": ind_base_runs,
                    "wickets": ind_wkts,
                    "overs": ind_overs,
                    "crr": crr,
                    "is_batting": True
                },
                "team2": {
                    "name": "Australia",
                    "short": "AUS",
                    "runs": 287,
                    "wickets": 8,
                    "overs": "50.0",
                    "crr": 5.74,
                    "is_batting": False
                },
                "target": 288,
                "summary": match_1_status,
                "required_rate": rrr,
                "current_batters": [
                    {"name": "Virat Kohli", "runs": kohli_runs, "balls": kohli_balls, "fours": 7, "sixes": 1, "on_strike": True},
                    {"name": "Hardik Pandya", "runs": hardik_runs, "balls": hardik_balls, "fours": 3, "sixes": 1, "on_strike": False}
                ],
                "current_bowler": {
                    "name": "Mitchell Starc",
                    "overs": "8.2",
                    "maidens": 0,
                    "runs": 54,
                    "wickets": 1
                }
            },
            {
                "id": "live_eng_sa_t20",
                "title": "England vs South Africa - 3rd T20I",
                "series": "South Africa Tour of England 2026",
                "format": "T20",
                "status": "LIVE",
                "is_live": True,
                "venue": "The Oval, London",
                "date": str(date.today()),
                "team1": {
                    "name": "South Africa",
                    "short": "SA",
                    "runs": sa_base_runs,
                    "wickets": sa_wkts,
                    "overs": sa_overs,
                    "crr": sa_crr,
                    "is_batting": True
                },
                "team2": {
                    "name": "England",
                    "short": "ENG",
                    "runs": 182,
                    "wickets": 6,
                    "overs": "20.0",
                    "crr": 9.10,
                    "is_batting": False
                },
                "target": 183,
                "summary": match_2_status,
                "required_rate": sa_rrr,
                "current_batters": [
                    {"name": "Heinrich Klaasen", "runs": klaasen_runs, "balls": klaasen_balls, "fours": 4, "sixes": 3, "on_strike": True},
                    {"name": "David Miller", "runs": 22, "balls": 15, "fours": 2, "sixes": 1, "on_strike": False}
                ],
                "current_bowler": {
                    "name": "Jofra Archer",
                    "overs": "3.4",
                    "maidens": 0,
                    "runs": 32,
                    "wickets": 2
                }
            },
            {
                "id": "live_nz_pak_test",
                "title": "New Zealand vs Pakistan - 1st Test",
                "series": "Pakistan Tour of New Zealand 2026",
                "format": "Test",
                "status": "LIVE",
                "is_live": True,
                "venue": "Basin Reserve, Wellington",
                "date": str(date.today()),
                "team1": {
                    "name": "Pakistan",
                    "short": "PAK",
                    "runs": pak_runs,
                    "wickets": 5,
                    "overs": pak_overs,
                    "innings_desc": "240 & 1st Inn",
                    "is_batting": True
                },
                "team2": {
                    "name": "New Zealand",
                    "short": "NZ",
                    "runs": 384,
                    "wickets": 10,
                    "overs": "112.4",
                    "innings_desc": "1st Inn",
                    "is_batting": False
                },
                "target": None,
                "summary": f"{lead_trail_text} (Day 4 - Final Session)",
                "current_batters": [
                    {"name": "Babar Azam", "runs": 71, "balls": 154, "fours": 8, "sixes": 0, "on_strike": True},
                    {"name": "Mohammad Rizwan", "runs": 38, "balls": 76, "fours": 4, "sixes": 0, "on_strike": False}
                ],
                "current_bowler": {
                    "name": "Tim Southee",
                    "overs": "16.0",
                    "maidens": 4,
                    "runs": 48,
                    "wickets": 2
                }
            }
        ]

    def import_live_match(self, match_data, db_adapter):
        """
        Imports a live match from the live feed into the local relational database.
        Resolves or creates teams, resolves venue, creates match & initial innings.
        """
        title = match_data.get("title") or "Live International Match"
        fmt = match_data.get("format", "T20")
        match_date = match_data.get("date", str(date.today()))
        venue_name = match_data.get("venue", "International Stadium")
        status = "In Progress"
        summary = match_data.get("summary", "Live match in progress")

        team1_info = match_data.get("team1", {})
        team2_info = match_data.get("team2", {})
        t1_name = team1_info.get("name", "Team 1")
        t2_name = team2_info.get("name", "Team 2")

        # 1. Resolve or create Team 1
        t1_row = db_adapter.query_one("SELECT team_id FROM teams WHERE team_name = %s", (t1_name,))
        if not t1_row:
            t1_id = db_adapter.execute("INSERT INTO teams (team_name, country, team_type) VALUES (%s, %s, 'International')", (t1_name, t1_name))
        else:
            t1_id = t1_row["team_id"]

        # 2. Resolve or create Team 2
        t2_row = db_adapter.query_one("SELECT team_id FROM teams WHERE team_name = %s", (t2_name,))
        if not t2_row:
            t2_id = db_adapter.execute("INSERT INTO teams (team_name, country, team_type) VALUES (%s, %s, 'International')", (t2_name, t2_name))
        else:
            t2_id = t2_row["team_id"]

        # 3. Resolve or create Venue
        venue_parts = [p.strip() for p in venue_name.split(",")]
        v_name = venue_parts[0]
        v_city = venue_parts[1] if len(venue_parts) > 1 else ""
        v_country = venue_parts[2] if len(venue_parts) > 2 else ""

        v_row = db_adapter.query_one("SELECT venue_id FROM venues WHERE venue_name LIKE %s", (f"%{v_name}%",))
        if not v_row:
            v_id = db_adapter.execute("INSERT INTO venues (venue_name, city, country) VALUES (%s, %s, %s)", (v_name, v_city, v_country))
        else:
            v_id = v_row["venue_id"]

        # 4. Check if already imported
        existing_match = db_adapter.query_one(
            "SELECT match_id FROM matches WHERE match_title = %s AND match_date = %s",
            (title, match_date)
        )
        if existing_match:
            # Update status & summary
            db_adapter.execute(
                "UPDATE matches SET status = %s, result_summary = %s WHERE match_id = %s",
                (status, summary, existing_match["match_id"])
            )
            return {"match_id": existing_match["match_id"], "is_new": False}

        # 5. Insert new match
        overs_limit = 20 if fmt == "T20" else (50 if fmt == "ODI" else None)
        new_match_id = db_adapter.execute("""
            INSERT INTO matches (match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, result_summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, fmt, match_date, v_id, t1_id, t2_id, overs_limit, status, summary))

        # 6. Add initial innings record if runs present
        if team2_info.get("runs"):
            # Innings 1 (Team 2 batted first)
            t2_overs = float(str(team2_info.get("overs", 0.0)).replace(" ov", ""))
            legal_balls = int(int(t2_overs) * 6 + round((t2_overs % 1) * 10))
            db_adapter.execute("""
                INSERT INTO innings (match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls)
                VALUES (%s, 1, %s, %s, %s, %s)
            """, (new_match_id, t2_id, team2_info.get("runs", 0), team2_info.get("wickets", 0), legal_balls))

        if team1_info.get("runs"):
            # Innings 2 (Team 1 currently batting)
            t1_overs = float(str(team1_info.get("overs", 0.0)).replace(" ov", ""))
            legal_balls = int(int(t1_overs) * 6 + round((t1_overs % 1) * 10))
            db_adapter.execute("""
                INSERT INTO innings (match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls)
                VALUES (%s, 2, %s, %s, %s, %s)
            """, (new_match_id, t1_id, team1_info.get("runs", 0), team1_info.get("wickets", 0), legal_balls))

        return {"match_id": new_match_id, "is_new": True}

# Singleton instance
cricket_api = CricketAPIClient()
