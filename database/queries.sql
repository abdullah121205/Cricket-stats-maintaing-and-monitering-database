USE cricket_stats;

-- 1. View all matches with team and venue names
SELECT
    m.match_id,
    m.match_title,
    m.format,
    m.match_date,
    t1.team_name AS team1,
    t2.team_name AS team2,
    v.venue_name,
    m.status
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN venues v ON m.venue_id = v.venue_id
ORDER BY m.match_date;

-- 2. View players assigned to each match
SELECT
    m.match_title,
    t.team_name,
    p.full_name,
    p.role,
    mp.captain,
    mp.wicketkeeper
FROM match_players mp
JOIN matches m ON mp.match_id = m.match_id
JOIN teams t ON mp.team_id = t.team_id
JOIN players p ON mp.player_id = p.player_id
ORDER BY m.match_id, t.team_name, p.full_name;

-- 3. Count matches by format
SELECT format, COUNT(*) AS total_matches
FROM matches
GROUP BY format;

-- 4. Count players by role
SELECT role, COUNT(*) AS total_players
FROM players
GROUP BY role
ORDER BY total_players DESC;

-- 5. Count matches by status
SELECT status, COUNT(*) AS total_matches
FROM matches
GROUP BY status;

-- 6. View upcoming scheduled matches
SELECT match_title, format, match_date
FROM matches
WHERE status = 'Scheduled'
ORDER BY match_date;

-- 7. View matches involving a selected team
SELECT
    match_title,
    format,
    match_date,
    status
FROM matches
WHERE team1_id = 1 OR team2_id = 1
ORDER BY match_date;

-- 8. Check for matches where both teams are the same
SELECT match_id, match_title
FROM matches
WHERE team1_id = team2_id;

-- ==========================================================
-- STATISTICAL & ANALYTICAL LEADERBOARD QUERIES
-- ==========================================================

-- 9. Top Run Scorers (Total Career Runs)
SELECT 
    p.player_id,
    p.full_name,
    p.nationality,
    COUNT(bs.batting_stat_id) AS innings_batted,
    SUM(bs.runs) AS total_runs,
    MAX(bs.runs) AS highest_score,
    ROUND(SUM(bs.runs) * 100.0 / NULLIF(SUM(bs.balls_faced), 0), 2) AS strike_rate,
    SUM(bs.fours) AS total_fours,
    SUM(bs.sixes) AS total_sixes
FROM players p
JOIN batting_stats bs ON p.player_id = bs.player_id
GROUP BY p.player_id, p.full_name, p.nationality
ORDER BY total_runs DESC;

-- 10. Top Wicket Takers (Total Career Wickets)
SELECT 
    p.player_id,
    p.full_name,
    p.nationality,
    SUM(bw.wickets) AS total_wickets,
    ROUND(SUM(bw.legal_balls) / 6.0, 1) AS overs_bowled,
    SUM(bw.runs_conceded) AS runs_conceded,
    ROUND(SUM(bw.runs_conceded) * 1.0 / NULLIF(SUM(bw.wickets), 0), 2) AS bowling_average,
    ROUND(SUM(bw.runs_conceded) * 6.0 / NULLIF(SUM(bw.legal_balls), 0), 2) AS economy_rate
FROM players p
JOIN bowling_stats bw ON p.player_id = bw.player_id
GROUP BY p.player_id, p.full_name, p.nationality
ORDER BY total_wickets DESC;

-- 11. Highest Individual Score in a Match Innings
SELECT 
    p.full_name,
    bs.runs,
    bs.balls_faced,
    bs.fours,
    bs.sixes,
    ROUND(bs.runs * 100.0 / NULLIF(bs.balls_faced, 0), 2) AS strike_rate,
    m.match_title,
    m.match_date
FROM batting_stats bs
JOIN players p ON bs.player_id = p.player_id
JOIN innings i ON bs.innings_id = i.innings_id
JOIN matches m ON i.match_id = m.match_id
ORDER BY bs.runs DESC
LIMIT 5;

-- 12. Best Strike Rates (Minimum 30 balls faced)
SELECT 
    p.full_name,
    SUM(bs.runs) AS total_runs,
    SUM(bs.balls_faced) AS balls_faced,
    ROUND(SUM(bs.runs) * 100.0 / SUM(bs.balls_faced), 2) AS strike_rate
FROM players p
JOIN batting_stats bs ON p.player_id = bs.player_id
GROUP BY p.player_id, p.full_name
HAVING balls_faced >= 30
ORDER BY strike_rate DESC;

-- 13. Team Win / Loss Record and Win Percentage
SELECT 
    t.team_name,
    t.country,
    COUNT(m.match_id) AS matches_played,
    SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN m.winner_team_id IS NOT NULL AND m.winner_team_id <> t.team_id THEN 1 ELSE 0 END) AS losses,
    ROUND(SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(m.match_id), 0), 2) AS win_percentage
FROM teams t
LEFT JOIN matches m ON (t.team_id = m.team1_id OR t.team_id = m.team2_id) AND m.status = 'Completed'
GROUP BY t.team_id, t.team_name, t.country
ORDER BY wins DESC, win_percentage DESC;

-- 14. Full Scorecard for a Match (e.g. Match ID 2)
SELECT 
    i.innings_number,
    bt.team_name AS batting_team,
    p.full_name AS batsman,
    bs.batting_position,
    bs.runs,
    bs.balls_faced,
    bs.fours,
    bs.sixes,
    bs.dismissal_kind
FROM innings i
JOIN teams bt ON i.batting_team_id = bt.team_id
JOIN batting_stats bs ON i.innings_id = bs.innings_id
JOIN players p ON bs.player_id = p.player_id
WHERE i.match_id = 2
ORDER BY i.innings_number, bs.batting_position;
