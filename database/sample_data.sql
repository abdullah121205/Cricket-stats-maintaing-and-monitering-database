USE cricket_stats;

-- 1. Add demo teams (Required by matches foreign key constraints)
INSERT INTO teams (team_id, team_name, country, team_type)
SELECT 1, 'India', 'India', 'International'
WHERE NOT EXISTS (SELECT 1 FROM teams WHERE team_name = 'India');

INSERT INTO teams (team_id, team_name, country, team_type)
SELECT 2, 'Australia', 'Australia', 'International'
WHERE NOT EXISTS (SELECT 1 FROM teams WHERE team_name = 'Australia');

INSERT INTO teams (team_id, team_name, country, team_type)
SELECT 3, 'England', 'England', 'International'
WHERE NOT EXISTS (SELECT 1 FROM teams WHERE team_name = 'England');

INSERT INTO teams (team_id, team_name, country, team_type)
SELECT 4, 'South Africa', 'South Africa', 'International'
WHERE NOT EXISTS (SELECT 1 FROM teams WHERE team_name = 'South Africa');

-- 2. Add demo players (preserves original players + international stars)
INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 1, 'Arjun Sharma', 'India', 'Batter', 'Right-hand bat', NULL
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Arjun Sharma');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 2, 'Rahul Kumar', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Rahul Kumar');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 3, 'Vikram Patel', 'India', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Vikram Patel');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 4, 'Liam Wilson', 'Australia', 'Batter', 'Right-hand bat', NULL
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Liam Wilson');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 5, 'Noah Taylor', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Noah Taylor');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 6, 'Oliver Brown', 'Australia', 'All-rounder', 'Right-hand bat', 'Right-arm medium'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Oliver Brown');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 7, 'Virat Kohli', 'India', 'Batter', 'Right-hand bat', 'Right-arm medium'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Virat Kohli');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 8, 'Rohit Sharma', 'India', 'Batter', 'Right-hand bat', 'Right-arm offbreak'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Rohit Sharma');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 9, 'Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Jasprit Bumrah');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 10, 'Steve Smith', 'Australia', 'Batter', 'Right-hand bat', 'Right-arm legbreak'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Steve Smith');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 11, 'Pat Cummins', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Pat Cummins');

INSERT INTO players (player_id, full_name, nationality, role, batting_style, bowling_style)
SELECT 12, 'Mitchell Starc', 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast'
WHERE NOT EXISTS (SELECT 1 FROM players WHERE full_name = 'Mitchell Starc');

-- 3. Add demo venues
INSERT INTO venues (venue_id, venue_name, city, country)
SELECT 1, 'National Cricket Ground', 'Chennai', 'India'
WHERE NOT EXISTS (SELECT 1 FROM venues WHERE venue_name = 'National Cricket Ground');

INSERT INTO venues (venue_id, venue_name, city, country)
SELECT 2, 'City Cricket Stadium', 'Mumbai', 'India'
WHERE NOT EXISTS (SELECT 1 FROM venues WHERE venue_name = 'City Cricket Stadium');

INSERT INTO venues (venue_id, venue_name, city, country)
SELECT 3, 'Harbour Cricket Ground', 'Sydney', 'Australia'
WHERE NOT EXISTS (SELECT 1 FROM venues WHERE venue_name = 'Harbour Cricket Ground');

INSERT INTO venues (venue_id, venue_name, city, country)
SELECT 4, 'Eden Gardens', 'Kolkata', 'India'
WHERE NOT EXISTS (SELECT 1 FROM venues WHERE venue_name = 'Eden Gardens');

-- 4. Add matches (including completed matches with winners for rich statistics)
INSERT INTO matches
    (match_id, match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, toss_winner_team_id, toss_decision, winner_team_id, result_type, result_summary, player_of_match_id)
SELECT
    1, 'India vs Australia - Test Demo', 'Test', '2026-03-10', 1, 1, 2, NULL, 'Completed', 1, 'Bat', 1, 'Runs', 'India won by 124 runs', 7
WHERE NOT EXISTS (SELECT 1 FROM matches WHERE match_id = 1);

INSERT INTO matches
    (match_id, match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, toss_winner_team_id, toss_decision, winner_team_id, result_type, result_summary, player_of_match_id)
SELECT
    2, 'India vs Australia - ODI Demo', 'ODI', '2026-03-18', 2, 1, 2, 50, 'Completed', 2, 'Bowl', 1, 'Runs', 'India won by 35 runs', 8
WHERE NOT EXISTS (SELECT 1 FROM matches WHERE match_id = 2);

INSERT INTO matches
    (match_id, match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, toss_winner_team_id, toss_decision, winner_team_id, result_type, result_summary, player_of_match_id)
SELECT
    3, 'Australia vs India - T20 Demo', 'T20', '2026-03-25', 3, 2, 1, 20, 'Completed', 1, 'Bowl', 2, 'Runs', 'Australia won by 14 runs', 10
WHERE NOT EXISTS (SELECT 1 FROM matches WHERE match_id = 3);

INSERT INTO matches
    (match_id, match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, toss_winner_team_id, toss_decision, winner_team_id, result_type, result_summary, player_of_match_id)
SELECT
    4, 'India vs England - ODI Clash', 'ODI', '2026-11-15', 4, 1, 3, 50, 'Scheduled', NULL, NULL, NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM matches WHERE match_id = 4);

-- 5. Add Match Players (Playing XI / Captains / Keepers)
INSERT INTO match_players (match_id, player_id, team_id, playing_xi, captain, wicketkeeper)
VALUES
(2, 7, 1, TRUE, FALSE, FALSE),
(2, 8, 1, TRUE, TRUE, FALSE),
(2, 9, 1, TRUE, FALSE, FALSE),
(2, 1, 1, TRUE, FALSE, FALSE),
(2, 2, 1, TRUE, FALSE, FALSE),
(2, 10, 2, TRUE, FALSE, FALSE),
(2, 11, 2, TRUE, TRUE, FALSE),
(2, 12, 2, TRUE, FALSE, FALSE),
(2, 4, 2, TRUE, FALSE, FALSE),
(2, 5, 2, TRUE, FALSE, FALSE);

-- 6. Add Innings for Match 2 (ODI Demo: India vs Australia)
INSERT INTO innings (innings_id, match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls)
VALUES
(1, 2, 1, 1, 312, 6, 300),
(2, 2, 2, 2, 277, 10, 284);

-- Add Innings for Match 3 (T20 Demo: Australia vs India)
INSERT INTO innings (innings_id, match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls)
VALUES
(3, 3, 1, 2, 186, 5, 120),
(4, 3, 2, 1, 172, 8, 120);

-- 7. Add Batting Stats
INSERT INTO batting_stats (innings_id, player_id, batting_position, runs, balls_faced, fours, sixes, is_out, dismissal_kind, bowler_player_id)
VALUES
-- Match 2, 1st Innings (India batting)
(1, 8, 1, 85, 78, 9, 3, TRUE, 'caught', 11),
(1, 1, 2, 34, 42, 4, 0, TRUE, 'bowled', 12),
(1, 7, 3, 112, 98, 11, 2, TRUE, 'caught', 11),
(1, 3, 4, 45, 36, 4, 2, FALSE, 'not out', NULL),

-- Match 2, 2nd Innings (Australia batting)
(2, 4, 1, 48, 52, 5, 1, TRUE, 'caught', 9),
(2, 10, 2, 94, 88, 10, 1, TRUE, 'lbw', 2),
(2, 6, 3, 52, 46, 4, 2, TRUE, 'bowled', 9),

-- Match 3, 1st Innings (Australia batting)
(3, 10, 1, 78, 48, 8, 3, TRUE, 'caught', 9),
(3, 6, 2, 44, 26, 3, 3, FALSE, 'not out', NULL),

-- Match 3, 2nd Innings (India batting)
(4, 8, 1, 54, 32, 6, 3, TRUE, 'caught', 12),
(4, 7, 2, 68, 44, 7, 2, TRUE, 'bowled', 11);

-- 8. Add Bowling Stats
INSERT INTO bowling_stats (innings_id, player_id, legal_balls, maidens, runs_conceded, wickets, wides, no_balls)
VALUES
-- Match 2, Australia bowling (Innings 1)
(1, 11, 60, 1, 58, 2, 1, 0),
(1, 12, 60, 0, 64, 1, 2, 0),
(1, 5, 48, 0, 52, 1, 0, 0),

-- Match 2, India bowling (Innings 2)
(2, 9, 58, 2, 44, 4, 1, 0),
(2, 2, 60, 0, 56, 2, 0, 0),
(2, 3, 48, 0, 48, 1, 1, 0),

-- Match 3, India bowling (Innings 1)
(3, 9, 24, 0, 28, 3, 0, 0),
(3, 2, 24, 0, 36, 1, 1, 0),

-- Match 3, Australia bowling (Innings 2)
(4, 11, 24, 0, 30, 2, 0, 0),
(4, 12, 24, 0, 38, 2, 1, 0);
