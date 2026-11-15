"""
Cricket External & Live API Integration Service
Provides real-time scores, CricAPI synchronization, dynamic live match simulation,
and one-click import into the local relational database.
"""

import os
import json
import time
from datetime import datetime, date
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from dotenv import load_dotenv

# Ensure .env is loaded regardless of import order
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class CricketAPIClient:
    def __init__(self, api_key=None, base_url="https://api.cricapi.com/v1"):
        self._api_key = api_key
        self.base_url = base_url

    @property
    def api_key(self):
        """Dynamically reads the API key from environment so it is never stale."""
        key = self._api_key or os.getenv("CRICKET_API_KEY", "")
        return key.strip() if key else ""

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def get_live_scores(self):
        """
        Fetches live international cricket matches.
        Uses CricAPI if CRICKET_API_KEY is configured; otherwise provides
        a dynamic, high-fidelity real-time simulation engine.
        """
        current_key = self.api_key
        if current_key and current_key != "YOUR_API_KEY_HERE":
            external_data = self._fetch_from_cricapi()
            if external_data and external_data.get("status") == "success":
                matches = external_data.get("data") or []
                if matches:
                    return {
                        "source": "cricapi",
                        "status": "success",
                        "count": len(matches),
                        "data": self._normalize_cricapi_matches(matches[:6])
                    }

        # Dynamic simulation fallback with realistic live progression
        return {
            "source": "live_engine",
            "status": "success",
            "message": "Live feed active (Dynamic Real-Time Simulation)",
            "has_api_key": bool(current_key and current_key != "YOUR_API_KEY_HERE"),
            "data": self._generate_simulated_live_matches()
        }

    def _fetch_from_cricapi(self):
        url = f"{self.base_url}/currentMatches?apikey={self.api_key}"
        try:
            req = Request(url, headers={"User-Agent": "CricketStatsDatabase/1.0"})
            with urlopen(req, timeout=12) as response:
                return json.loads(response.read().decode())
        except (URLError, Exception) as e:
            print(f"[CricketAPI Warning] External fetch failed: {e}")
            return None

    def _normalize_cricapi_matches(self, matches):
        normalized = []
        for m in matches:
            teams = m.get("teams") or []
            t1_name = teams[0] if len(teams) > 0 else "Team 1"
            t2_name = teams[1] if len(teams) > 1 else "Team 2"
            
            score_entries = m.get("score") or []
            t1_score = {}
            t2_score = {}
            if len(score_entries) >= 2:
                t1_score = score_entries[0]
                t2_score = score_entries[1]
            elif len(score_entries) == 1:
                t1_score = score_entries[0]

            is_live = bool(m.get("matchStarted", False)) and not bool(m.get("matchEnded", False))
            status_text = m.get("status") or ("LIVE" if is_live else "Scheduled")

            normalized.append({
                "id": m.get("id"),
                "title": m.get("name") or f"{t1_name} vs {t2_name}",
                "format": (m.get("matchType") or "T20").upper(),
                "status": "LIVE" if is_live else status_text,
                "is_live": is_live,
                "venue": m.get("venue") or "International Cricket Ground",
                "date": m.get("date") or str(date.today()),
                "team1": {
                    "name": t1_name,
                    "runs": t1_score.get("r", 0) if t1_score else "-",
                    "wickets": t1_score.get("w", 0) if t1_score else "-",
                    "overs": t1_score.get("o", 0.0) if t1_score else "",
                    "is_batting": is_live and (t1_score.get("r") is not None)
                },
                "team2": {
                    "name": t2_name,
                    "runs": t2_score.get("r", 0) if t2_score else "-",
                    "wickets": t2_score.get("w", 0) if t2_score else "-",
                    "overs": t2_score.get("o", 0.0) if t2_score else "",
                    "is_batting": False
                },
                "summary": status_text,
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

    def _parse_int(self, val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    def _parse_overs_to_balls(self, overs_val):
        try:
            ov_str = str(overs_val).replace(" ov", "").strip()
            ov = float(ov_str)
            return int(int(ov) * 6 + round((ov % 1) * 10))
        except (ValueError, TypeError):
            return 0

    def _sync_innings_score(self, match_id, innings_number, team_id, team_info, db_adapter):
        runs = self._parse_int(team_info.get("runs"))
        wickets = self._parse_int(team_info.get("wickets"))
        legal_balls = self._parse_overs_to_balls(team_info.get("overs"))
        
        if runs <= 0 and wickets <= 0 and legal_balls <= 0:
            return

        existing = db_adapter.query_one(
            "SELECT innings_id FROM innings WHERE match_id = %s AND innings_number = %s",
            (match_id, innings_number)
        )
        if existing:
            db_adapter.execute("""
                UPDATE innings 
                SET batting_team_id = %s, total_runs = %s, wickets_lost = %s, legal_balls = %s
                WHERE innings_id = %s
            """, (team_id, runs, wickets, legal_balls, existing["innings_id"]))
        else:
            db_adapter.execute("""
                INSERT INTO innings (match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (match_id, innings_number, team_id, runs, wickets, legal_balls))

    def _sync_live_players_and_stats(self, match_id, t1_id, t2_id, match_data, db_adapter):
        """
        Automatically adds/updates live batters and bowlers in the players table,
        assigns them to match_players, and records their live batting and bowling stats.
        """
        batters = match_data.get("current_batters") or []
        bowler = match_data.get("current_bowler")
        team1_info = match_data.get("team1") or {}
        team2_info = match_data.get("team2") or {}

        # Determine which team is batting
        t1_is_batting = team1_info.get("is_batting", True)
        batting_team_id = t1_id if t1_is_batting else t2_id
        bowling_team_id = t2_id if t1_is_batting else t1_id
        batting_team_name = team1_info.get("name") if t1_is_batting else team2_info.get("name")
        bowling_team_name = team2_info.get("name") if t1_is_batting else team1_info.get("name")

        # Find the active innings for the batting team
        inn_row = db_adapter.query_one(
            "SELECT innings_id FROM innings WHERE match_id = %s AND batting_team_id = %s",
            (match_id, batting_team_id)
        )
        inn_id = inn_row["innings_id"] if inn_row else None

        # 1. Sync Batters
        for b_pos, b in enumerate(batters, start=1):
            p_name = (b.get("name") or "").strip()
            if not p_name:
                continue

            # Ensure player exists
            p_row = db_adapter.query_one("SELECT player_id FROM players WHERE full_name = %s", (p_name,))
            if not p_row:
                p_id = db_adapter.execute("""
                    INSERT INTO players (full_name, nationality, role, is_active)
                    VALUES (%s, %s, 'Batter', 1)
                """, (p_name, batting_team_name or "International"))
            else:
                p_id = p_row["player_id"]

            # Ensure in match_players
            mp_row = db_adapter.query_one(
                "SELECT match_player_id FROM match_players WHERE match_id = %s AND player_id = %s",
                (match_id, p_id)
            )
            if not mp_row:
                db_adapter.execute("""
                    INSERT INTO match_players (match_id, player_id, team_id, playing_xi)
                    VALUES (%s, %s, %s, 1)
                """, (match_id, p_id, batting_team_id))

            # Record in batting_stats
            if inn_id:
                runs = self._parse_int(b.get("runs", 0))
                balls = self._parse_int(b.get("balls", 0))
                fours = self._parse_int(b.get("fours", 0))
                sixes = self._parse_int(b.get("sixes", 0))

                bs_row = db_adapter.query_one(
                    "SELECT batting_stat_id FROM batting_stats WHERE innings_id = %s AND player_id = %s",
                    (inn_id, p_id)
                )
                if bs_row:
                    db_adapter.execute("""
                        UPDATE batting_stats
                        SET runs = %s, balls_faced = %s, fours = %s, sixes = %s, is_out = 0, batting_position = %s
                        WHERE batting_stat_id = %s
                    """, (runs, balls, fours, sixes, b_pos, bs_row["batting_stat_id"]))
                else:
                    db_adapter.execute("""
                        INSERT INTO batting_stats (innings_id, player_id, batting_position, runs, balls_faced, fours, sixes, is_out, dismissal_kind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 'not out')
                    """, (inn_id, p_id, b_pos, runs, balls, fours, sixes))

        # 2. Sync Bowler
        if bowler:
            bw_name = (bowler.get("name") or "").strip()
            if bw_name:
                bw_p_row = db_adapter.query_one("SELECT player_id FROM players WHERE full_name = %s", (bw_name,))
                if not bw_p_row:
                    bw_p_id = db_adapter.execute("""
                        INSERT INTO players (full_name, nationality, role, is_active)
                        VALUES (%s, %s, 'Bowler', 1)
                    """, (bw_name, bowling_team_name or "International"))
                else:
                    bw_p_id = bw_p_row["player_id"]

                # Ensure in match_players
                mp_row = db_adapter.query_one(
                    "SELECT match_player_id FROM match_players WHERE match_id = %s AND player_id = %s",
                    (match_id, bw_p_id)
                )
                if not mp_row:
                    db_adapter.execute("""
                        INSERT INTO match_players (match_id, player_id, team_id, playing_xi)
                        VALUES (%s, %s, %s, 1)
                    """, (match_id, bw_p_id, bowling_team_id))

                # Record in bowling_stats
                if inn_id:
                    legal_balls = self._parse_overs_to_balls(bowler.get("overs", 0))
                    maidens = self._parse_int(bowler.get("maidens", 0))
                    runs_conceded = self._parse_int(bowler.get("runs", 0))
                    wickets = self._parse_int(bowler.get("wickets", 0))

                    bw_stat_row = db_adapter.query_one(
                        "SELECT bowling_stat_id FROM bowling_stats WHERE innings_id = %s AND player_id = %s",
                        (inn_id, bw_p_id)
                    )
                    if bw_stat_row:
                        db_adapter.execute("""
                            UPDATE bowling_stats
                            SET legal_balls = %s, maidens = %s, runs_conceded = %s, wickets = %s
                            WHERE bowling_stat_id = %s
                        """, (legal_balls, maidens, runs_conceded, wickets, bw_stat_row["bowling_stat_id"]))
                    else:
                        db_adapter.execute("""
                            INSERT INTO bowling_stats (innings_id, player_id, legal_balls, maidens, runs_conceded, wickets)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (inn_id, bw_p_id, legal_balls, maidens, runs_conceded, wickets))

    def fetch_match_scorecard(self, cricapi_id):
        """Fetches full match scorecard from CricAPI for given match id."""
        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            return None
        url = f"{self.base_url}/match_scorecard?apikey={self.api_key}&id={cricapi_id}"
        try:
            req = Request(url, headers={"User-Agent": "CricketStats/1.0"})
            with urlopen(req, timeout=12) as response:
                res = json.loads(response.read().decode())
                if res.get("status") == "success":
                    return res.get("data")
        except Exception as e:
            print(f"[CricketAPI Warning] Could not fetch scorecard for {cricapi_id}: {e}")
        return None

    def _sync_cricapi_scorecard_to_db(self, match_id, t1_id, t2_id, t1_name, t2_name, sc_data, db_adapter):
        """
        Syncs full CricAPI scorecard: all innings, real batters, bowlers, and playing XIs into the database.
        """
        scorecards = sc_data.get("scorecard", [])
        if not scorecards:
            return

        for inn_idx, inn in enumerate(scorecards, start=1):
            inn_title = (inn.get("inning") or "").lower()
            
            # Determine batting and bowling team
            if t1_name.lower() in inn_title:
                batting_team_id, bowling_team_id = t1_id, t2_id
                batting_nat, bowling_nat = t1_name, t2_name
            elif t2_name.lower() in inn_title:
                batting_team_id, bowling_team_id = t2_id, t1_id
                batting_nat, bowling_nat = t2_name, t1_name
            else:
                if inn_idx % 2 == 1:
                    batting_team_id, bowling_team_id = t1_id, t2_id
                    batting_nat, bowling_nat = t1_name, t2_name
                else:
                    batting_team_id, bowling_team_id = t2_id, t1_id
                    batting_nat, bowling_nat = t2_name, t1_name

            batters = inn.get("batting", [])
            bowlers = inn.get("bowling", [])

            total_runs = sum(self._parse_int(b.get("r", 0)) for b in batters)
            wickets_lost = sum(1 for b in batters if b.get("dismissal") and b.get("dismissal") != "not out")
            legal_balls = sum(self._parse_overs_to_balls(bw.get("o", 0)) for bw in bowlers)

            # Ensure innings record exists
            inn_row = db_adapter.query_one(
                "SELECT innings_id FROM innings WHERE match_id = %s AND innings_number = %s",
                (match_id, inn_idx)
            )
            if inn_row:
                inn_id = inn_row["innings_id"]
                db_adapter.execute("""
                    UPDATE innings
                    SET batting_team_id = %s, total_runs = %s, wickets_lost = %s, legal_balls = %s
                    WHERE innings_id = %s
                """, (batting_team_id, total_runs, wickets_lost, legal_balls, inn_id))
            else:
                inn_id = db_adapter.execute("""
                    INSERT INTO innings (match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (match_id, inn_idx, batting_team_id, total_runs, wickets_lost, legal_balls))

            # Sync batters
            for pos, b in enumerate(batters, start=1):
                p_info = b.get("batsman") or {}
                p_name = (p_info.get("name") or "").strip()
                if not p_name:
                    continue

                p_row = db_adapter.query_one("SELECT player_id FROM players WHERE full_name = %s", (p_name,))
                if not p_row:
                    p_id = db_adapter.execute("""
                        INSERT INTO players (full_name, nationality, role, is_active)
                        VALUES (%s, %s, 'Batter', 1)
                    """, (p_name, batting_nat))
                else:
                    p_id = p_row["player_id"]

                # Link in match_players
                mp = db_adapter.query_one(
                    "SELECT match_player_id FROM match_players WHERE match_id = %s AND player_id = %s",
                    (match_id, p_id)
                )
                if not mp:
                    db_adapter.execute("""
                        INSERT INTO match_players (match_id, player_id, team_id, playing_xi)
                        VALUES (%s, %s, %s, 1)
                    """, (match_id, p_id, batting_team_id))

                # Insert/update batting_stats
                runs = self._parse_int(b.get("r", 0))
                balls = self._parse_int(b.get("b", 0))
                fours = self._parse_int(b.get("4s", 0))
                sixes = self._parse_int(b.get("6s", 0))
                d_type = (b.get("dismissal") or "").strip()
                is_out = 1 if (d_type and d_type.lower() != "not out") else 0
                d_text = b.get("dismissal-text") or (d_type if is_out else "not out")

                bs_row = db_adapter.query_one(
                    "SELECT batting_stat_id FROM batting_stats WHERE innings_id = %s AND player_id = %s",
                    (inn_id, p_id)
                )
                if bs_row:
                    db_adapter.execute("""
                        UPDATE batting_stats
                        SET runs = %s, balls_faced = %s, fours = %s, sixes = %s, is_out = %s, dismissal_kind = %s, batting_position = %s
                        WHERE batting_stat_id = %s
                    """, (runs, balls, fours, sixes, is_out, d_text, pos, bs_row["batting_stat_id"]))
                else:
                    db_adapter.execute("""
                        INSERT INTO batting_stats (innings_id, player_id, batting_position, runs, balls_faced, fours, sixes, is_out, dismissal_kind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (inn_id, p_id, pos, runs, balls, fours, sixes, is_out, d_text))

            # Sync bowlers
            for bw in bowlers:
                bw_info = bw.get("bowler") or {}
                bw_name = (bw_info.get("name") or "").strip()
                if not bw_name:
                    continue

                bw_p_row = db_adapter.query_one("SELECT player_id FROM players WHERE full_name = %s", (bw_name,))
                if not bw_p_row:
                    bw_p_id = db_adapter.execute("""
                        INSERT INTO players (full_name, nationality, role, is_active)
                        VALUES (%s, %s, 'Bowler', 1)
                    """, (bw_name, bowling_nat))
                else:
                    bw_p_id = bw_p_row["player_id"]

                # Link in match_players
                mp = db_adapter.query_one(
                    "SELECT match_player_id FROM match_players WHERE match_id = %s AND player_id = %s",
                    (match_id, bw_p_id)
                )
                if not mp:
                    db_adapter.execute("""
                        INSERT INTO match_players (match_id, player_id, team_id, playing_xi)
                        VALUES (%s, %s, %s, 1)
                    """, (match_id, bw_p_id, bowling_team_id))

                # Insert/update bowling_stats
                legal_balls = self._parse_overs_to_balls(bw.get("o", 0))
                maidens = self._parse_int(bw.get("m", 0))
                runs_conceded = self._parse_int(bw.get("r", 0))
                wickets = self._parse_int(bw.get("w", 0))

                bw_stat_row = db_adapter.query_one(
                    "SELECT bowling_stat_id FROM bowling_stats WHERE innings_id = %s AND player_id = %s",
                    (inn_id, bw_p_id)
                )
                if bw_stat_row:
                    db_adapter.execute("""
                        UPDATE bowling_stats
                        SET legal_balls = %s, maidens = %s, runs_conceded = %s, wickets = %s
                        WHERE bowling_stat_id = %s
                    """, (legal_balls, maidens, runs_conceded, wickets, bw_stat_row["bowling_stat_id"]))
                else:
                    db_adapter.execute("""
                        INSERT INTO bowling_stats (innings_id, player_id, legal_balls, maidens, runs_conceded, wickets)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (inn_id, bw_p_id, legal_balls, maidens, runs_conceded, wickets))

    def import_live_match(self, match_data, db_adapter):
        """
        Imports or updates a live match from the live feed into the local database.
        Resolves or creates teams, resolves venue, updates status, winner, and innings scores.
        """
        title = match_data.get("title") or "Live International Match"
        fmt = match_data.get("format", "T20")
        match_date = match_data.get("date", str(date.today()))
        venue_name = match_data.get("venue", "International Stadium")
        summary = match_data.get("summary", "Match in progress")

        # Determine status
        is_completed = "won" in summary.lower() or "tied" in summary.lower() or "drawn" in summary.lower()
        status = "Completed" if is_completed else ("In Progress" if match_data.get("is_live", True) else "Scheduled")

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

        # Determine winner if completed
        winner_team_id = None
        if is_completed:
            if t1_name.lower() in summary.lower() and "won" in summary.lower():
                winner_team_id = t1_id
            elif t2_name.lower() in summary.lower() and "won" in summary.lower():
                winner_team_id = t2_id

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

        # 4. Check if already recorded (match by title or title+date)
        existing_match = db_adapter.query_one(
            "SELECT match_id FROM matches WHERE match_title = %s",
            (title,)
        )
        if existing_match:
            match_id = existing_match["match_id"]
            db_adapter.execute("""
                UPDATE matches 
                SET status = %s, result_summary = %s, winner_team_id = COALESCE(%s, winner_team_id)
                WHERE match_id = %s
            """, (status, summary, winner_team_id, match_id))
            
            cric_id = match_data.get("id")
            if cric_id and not str(cric_id).startswith("live_"):
                sc_data = self.fetch_match_scorecard(cric_id)
                if sc_data:
                    self._sync_cricapi_scorecard_to_db(match_id, t1_id, t2_id, t1_name, t2_name, sc_data, db_adapter)
                else:
                    self._sync_innings_score(match_id, 1, t2_id, team2_info, db_adapter)
                    self._sync_innings_score(match_id, 2, t1_id, team1_info, db_adapter)
                    self._sync_live_players_and_stats(match_id, t1_id, t2_id, match_data, db_adapter)
            else:
                self._sync_innings_score(match_id, 1, t2_id, team2_info, db_adapter)
                self._sync_innings_score(match_id, 2, t1_id, team1_info, db_adapter)
                self._sync_live_players_and_stats(match_id, t1_id, t2_id, match_data, db_adapter)

            return {"match_id": match_id, "is_new": False}

        # 5. Insert new match
        overs_limit = 20 if fmt == "T20" else (50 if fmt == "ODI" else None)
        new_match_id = db_adapter.execute("""
            INSERT INTO matches (match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, winner_team_id, result_summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, fmt, match_date, v_id, t1_id, t2_id, overs_limit, status, winner_team_id, summary))

        # 6. Sync innings & detailed scorecards
        cric_id = match_data.get("id")
        if cric_id and not str(cric_id).startswith("live_"):
            sc_data = self.fetch_match_scorecard(cric_id)
            if sc_data:
                self._sync_cricapi_scorecard_to_db(new_match_id, t1_id, t2_id, t1_name, t2_name, sc_data, db_adapter)
            else:
                self._sync_innings_score(new_match_id, 1, t2_id, team2_info, db_adapter)
                self._sync_innings_score(new_match_id, 2, t1_id, team1_info, db_adapter)
                self._sync_live_players_and_stats(new_match_id, t1_id, t2_id, match_data, db_adapter)
        else:
            self._sync_innings_score(new_match_id, 1, t2_id, team2_info, db_adapter)
            self._sync_innings_score(new_match_id, 2, t1_id, team1_info, db_adapter)
            self._sync_live_players_and_stats(new_match_id, t1_id, t2_id, match_data, db_adapter)

        return {"match_id": new_match_id, "is_new": True}

# Singleton instance
cricket_api = CricketAPIClient()
