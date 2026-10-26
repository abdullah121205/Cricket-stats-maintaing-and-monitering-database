import sqlite3
import os
import re
from pathlib import Path
from backend.config import Config, BASE_DIR

try:
    import pymysql
    import pymysql.cursors
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False


class Database:
    _connection = None
    _engine = "sqlite"

    @classmethod
    def get_connection(cls):
        if Config.DB_TYPE == "mysql" and PYMYSQL_AVAILABLE:
            try:
                conn = pymysql.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )
                cls._engine = "mysql"
                return conn
            except Exception as e:
                print(f"[DB Warning] Could not connect to MySQL ({e}). Using SQLite fallback.")

        # Default SQLite
        cls._engine = "sqlite"
        db_path = Config.SQLITE_DB_PATH
        db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @classmethod
    def execute(cls, sql: str, params=None):
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            if cls._engine == "sqlite":
                sql_adapted = sql.replace("%s", "?")
                cur.execute(sql_adapted, params or ())
                last_id = cur.lastrowid
                conn.commit()
                return last_id
            else:
                cur.execute(sql, params or ())
                last_id = cur.lastrowid
                return last_id
        finally:
            conn.close()

    @classmethod
    def query_all(cls, sql: str, params=None):
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            if cls._engine == "sqlite":
                sql_adapted = sql.replace("%s", "?")
                cur.execute(sql_adapted, params or ())
                rows = cur.fetchall()
                return [dict(row) for row in rows]
            else:
                cur.execute(sql, params or ())
                return cur.fetchall()
        finally:
            conn.close()

    @classmethod
    def query_one(cls, sql: str, params=None):
        rows = cls.query_all(sql, params)
        return rows[0] if rows else None

    @classmethod
    def init_db(cls):
        """Initializes database schema and seed data if not present."""
        if Config.DB_TYPE == "sqlite" or cls._engine == "sqlite":
            cls._init_sqlite()

    @classmethod
    def _init_sqlite(cls):
        db_path = Config.SQLITE_DB_PATH
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='teams';")
        table_exists = cur.fetchone()

        if not table_exists:
            print("[DB] Initializing SQLite tables based on schema.sql...")
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS teams (
                team_id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT NOT NULL UNIQUE,
                country TEXT,
                team_type TEXT NOT NULL DEFAULT 'International',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                date_of_birth DATE,
                nationality TEXT,
                role TEXT NOT NULL,
                batting_style TEXT,
                bowling_style TEXT,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS venues (
                venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                venue_name TEXT NOT NULL,
                city TEXT,
                country TEXT,
                UNIQUE (venue_name, city, country)
            );

            CREATE TABLE IF NOT EXISTS matches (
                match_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_title TEXT,
                format TEXT NOT NULL,
                match_date DATE NOT NULL,
                venue_id INTEGER,
                team1_id INTEGER NOT NULL,
                team2_id INTEGER NOT NULL,
                overs_limit INTEGER,
                status TEXT NOT NULL DEFAULT 'Scheduled',
                toss_winner_team_id INTEGER,
                toss_decision TEXT,
                winner_team_id INTEGER,
                result_type TEXT,
                result_summary TEXT,
                player_of_match_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
                FOREIGN KEY (team1_id) REFERENCES teams(team_id),
                FOREIGN KEY (team2_id) REFERENCES teams(team_id),
                FOREIGN KEY (toss_winner_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (winner_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (player_of_match_id) REFERENCES players(player_id)
            );

            CREATE TABLE IF NOT EXISTS match_players (
                match_player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                team_id INTEGER NOT NULL,
                playing_xi BOOLEAN NOT NULL DEFAULT 1,
                captain BOOLEAN NOT NULL DEFAULT 0,
                wicketkeeper BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id),
                UNIQUE (match_id, player_id)
            );

            CREATE TABLE IF NOT EXISTS innings (
                innings_id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                innings_number INTEGER NOT NULL,
                batting_team_id INTEGER NOT NULL,
                total_runs INTEGER NOT NULL DEFAULT 0,
                wickets_lost INTEGER NOT NULL DEFAULT 0,
                legal_balls INTEGER NOT NULL DEFAULT 0,
                byes INTEGER NOT NULL DEFAULT 0,
                leg_byes INTEGER NOT NULL DEFAULT 0,
                wides INTEGER NOT NULL DEFAULT 0,
                no_balls INTEGER NOT NULL DEFAULT 0,
                penalty_runs INTEGER NOT NULL DEFAULT 0,
                declared BOOLEAN NOT NULL DEFAULT 0,
                forfeited BOOLEAN NOT NULL DEFAULT 0,
                FOREIGN KEY (match_id) REFERENCES matches(match_id),
                FOREIGN KEY (batting_team_id) REFERENCES teams(team_id),
                UNIQUE (match_id, innings_number)
            );

            CREATE TABLE IF NOT EXISTS batting_stats (
                batting_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                innings_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                batting_position INTEGER,
                runs INTEGER NOT NULL DEFAULT 0,
                balls_faced INTEGER NOT NULL DEFAULT 0,
                fours INTEGER NOT NULL DEFAULT 0,
                sixes INTEGER NOT NULL DEFAULT 0,
                is_out BOOLEAN NOT NULL DEFAULT 0,
                dismissal_kind TEXT,
                bowler_player_id INTEGER,
                fielder_player_id INTEGER,
                FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                FOREIGN KEY (bowler_player_id) REFERENCES players(player_id),
                FOREIGN KEY (fielder_player_id) REFERENCES players(player_id),
                UNIQUE (innings_id, player_id)
            );

            CREATE TABLE IF NOT EXISTS bowling_stats (
                bowling_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                innings_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                legal_balls INTEGER NOT NULL DEFAULT 0,
                maidens INTEGER NOT NULL DEFAULT 0,
                runs_conceded INTEGER NOT NULL DEFAULT 0,
                wickets INTEGER NOT NULL DEFAULT 0,
                wides INTEGER NOT NULL DEFAULT 0,
                no_balls INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
                FOREIGN KEY (player_id) REFERENCES players(player_id),
                UNIQUE (innings_id, player_id)
            );
            """)
            conn.commit()

            sample_data_file = BASE_DIR / "database" / "sample_data.sql"
            if sample_data_file.exists():
                print("[DB] Loading sample data from sample_data.sql into SQLite...")
                try:
                    with open(sample_data_file, "r", encoding="utf-8") as f:
                        lines = [line for line in f if not line.strip().startswith("USE ")]
                        content = "".join(lines)
                    cur.executescript(content)
                    conn.commit()
                    print("[DB] Sample data loaded successfully.")
                except Exception as ex:
                    print(f"[DB Seed Warning] error loading data: {ex}")
        conn.close()
