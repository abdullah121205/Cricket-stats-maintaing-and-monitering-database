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