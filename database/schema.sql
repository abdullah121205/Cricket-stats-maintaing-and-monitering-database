CREATE DATABASE IF NOT EXISTS cricket_stats;
USE cricket_stats;

-- 1. Teams
CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100),
    team_type ENUM('International', 'Domestic', 'Franchise')
        NOT NULL DEFAULT 'International',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Players
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    date_of_birth DATE,
    nationality VARCHAR(100),
    role ENUM('Batter', 'Bowler', 'All-rounder', 'Wicketkeeper')
        NOT NULL,
    batting_style VARCHAR(50),
    bowling_style VARCHAR(70),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_player_name (full_name)
);

-- 3. Venues
CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    UNIQUE KEY uq_venue (venue_name, city, country)
);

-- 4. Matches
CREATE TABLE matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    match_title VARCHAR(200),
    format ENUM('Test', 'ODI', 'T20') NOT NULL,
    match_date DATE NOT NULL,
    venue_id INT,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    overs_limit SMALLINT,
    status ENUM('Scheduled', 'In Progress', 'Completed', 'Abandoned')
        NOT NULL DEFAULT 'Scheduled',
    toss_winner_team_id INT,
    toss_decision ENUM('Bat', 'Bowl'),
    winner_team_id INT,
    result_type ENUM('Runs', 'Wickets', 'Draw', 'Tie', 'No Result'),
    result_summary VARCHAR(255),
    player_of_match_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (toss_winner_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_of_match_id) REFERENCES players(player_id),

    CONSTRAINT chk_different_teams CHECK (team1_id <> team2_id),
    CONSTRAINT chk_overs_limit CHECK (
        overs_limit IS NULL OR overs_limit > 0
    ),
    INDEX idx_match_date (match_date),
    INDEX idx_match_format_status (format, status)
);

-- 5. Players selected for each match
CREATE TABLE match_players (
    match_player_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    playing_xi BOOLEAN NOT NULL DEFAULT TRUE,
    captain BOOLEAN NOT NULL DEFAULT FALSE,
    wicketkeeper BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    UNIQUE KEY uq_match_player (match_id, player_id),
    INDEX idx_match_team (match_id, team_id)
);

-- 6. Innings
CREATE TABLE innings (
    innings_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    innings_number TINYINT NOT NULL,
    batting_team_id INT NOT NULL,
    total_runs INT NOT NULL DEFAULT 0,
    wickets_lost TINYINT NOT NULL DEFAULT 0,
    legal_balls INT NOT NULL DEFAULT 0,
    byes INT NOT NULL DEFAULT 0,
    leg_byes INT NOT NULL DEFAULT 0,
    wides INT NOT NULL DEFAULT 0,
    no_balls INT NOT NULL DEFAULT 0,
    penalty_runs INT NOT NULL DEFAULT 0,
    declared BOOLEAN NOT NULL DEFAULT FALSE,
    forfeited BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (batting_team_id) REFERENCES teams(team_id),
    UNIQUE KEY uq_match_innings (match_id, innings_number),

    CONSTRAINT chk_innings_number CHECK (innings_number > 0),
    CONSTRAINT chk_innings_totals CHECK (
        total_runs >= 0
        AND wickets_lost BETWEEN 0 AND 10
        AND legal_balls >= 0
        AND byes >= 0
        AND leg_byes >= 0
        AND wides >= 0
        AND no_balls >= 0
        AND penalty_runs >= 0
    )
);

-- 7. Batting scorecard
CREATE TABLE batting_stats (
    batting_stat_id INT AUTO_INCREMENT PRIMARY KEY,
    innings_id INT NOT NULL,
    player_id INT NOT NULL,
    batting_position TINYINT,
    runs INT NOT NULL DEFAULT 0,
    balls_faced INT NOT NULL DEFAULT 0,
    fours INT NOT NULL DEFAULT 0,
    sixes INT NOT NULL DEFAULT 0,
    is_out BOOLEAN NOT NULL DEFAULT FALSE,
    dismissal_kind VARCHAR(40),
    bowler_player_id INT,
    fielder_player_id INT,

    FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (bowler_player_id) REFERENCES players(player_id),
    FOREIGN KEY (fielder_player_id) REFERENCES players(player_id),
    UNIQUE KEY uq_innings_batter (innings_id, player_id),

    CONSTRAINT chk_batting_values CHECK (
        runs >= 0 AND balls_faced >= 0
        AND fours >= 0 AND sixes >= 0
    )
);

-- 8. Bowling scorecard
CREATE TABLE bowling_stats (
    bowling_stat_id INT AUTO_INCREMENT PRIMARY KEY,
    innings_id INT NOT NULL,
    player_id INT NOT NULL,
    legal_balls INT NOT NULL DEFAULT 0,
    maidens INT NOT NULL DEFAULT 0,
    runs_conceded INT NOT NULL DEFAULT 0,
    wickets INT NOT NULL DEFAULT 0,
    wides INT NOT NULL DEFAULT 0,
    no_balls INT NOT NULL DEFAULT 0,

    FOREIGN KEY (innings_id) REFERENCES innings(innings_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE KEY uq_innings_bowler (innings_id, player_id),

    CONSTRAINT chk_bowling_values CHECK (
        legal_balls >= 0 AND maidens >= 0
        AND runs_conceded >= 0 AND wickets >= 0
        AND wides >= 0 AND no_balls >= 0
    )
);

-- Confirm that the tables exist
SHOW TABLES;