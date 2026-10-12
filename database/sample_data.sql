USE cricket_stats;

-- Add demo players only if they do not already exist.
INSERT INTO players (full_name, nationality, role, batting_style, bowling_style)
SELECT 'Arjun Sharma', 'India', 'Batter', 'Right-hand bat', NULL
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE full_name = 'Arjun Sharma'
);

INSERT INTO players (full_name, nationality, role, batting_style, bowling_style)
SELECT 'Rahul Kumar', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast'
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE full_name = 'Rahul Kumar'
);

INSERT INTO players (full_name, nationality, role, batting_style, bowling_style)
SELECT 'Vikram Patel', 'India', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox'
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE full_name = 'Vikram Patel'
);

INSERT INTO players (full_name, nationality, role, batting_style, bowling_style)
SELECT 'Liam Wilson', 'Australia', 'Batter', 'Right-hand bat', NULL
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE full_name = 'Liam Wilson'
);

INSERT INTO players (full_name, nationality, role, batting_style, bowling_style)
SELECT 'Noah Taylor', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast'
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE full_name = 'Noah Taylor'
);

INSERT INTO players (full_name, nationality, role, batting_style, bowling_style)
SELECT 'Oliver Brown', 'Australia', 'All-rounder', 'Right-hand bat', 'Right-arm medium'
WHERE NOT EXISTS (
    SELECT 1 FROM players WHERE full_name = 'Oliver Brown'
);

-- Add demo venues if they do not already exist.
INSERT INTO venues (venue_name, city, country)
SELECT 'National Cricket Ground', 'Chennai', 'India'
WHERE NOT EXISTS (
    SELECT 1 FROM venues WHERE venue_name = 'National Cricket Ground'
);

INSERT INTO venues (venue_name, city, country)
SELECT 'City Cricket Stadium', 'Mumbai', 'India'
WHERE NOT EXISTS (
    SELECT 1 FROM venues WHERE venue_name = 'City Cricket Stadium'
);

INSERT INTO venues (venue_name, city, country)
SELECT 'Harbour Cricket Ground', 'Sydney', 'Australia'
WHERE NOT EXISTS (
    SELECT 1 FROM venues WHERE venue_name = 'Harbour Cricket Ground'
);

-- Add one demo match for each format if it does not already exist.
INSERT INTO matches
    (match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status)
SELECT
    'India vs Australia - Test Demo', 'Test', '2026-11-10',
    (SELECT venue_id FROM venues WHERE venue_name = 'National Cricket Ground' LIMIT 1),
    1, 2, NULL, 'Scheduled'
WHERE NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_title = 'India vs Australia - Test Demo'
);

INSERT INTO matches
    (match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status)
SELECT
    'India vs Australia - ODI Demo', 'ODI', '2026-11-15',
    (SELECT venue_id FROM venues WHERE venue_name = 'City Cricket Stadium' LIMIT 1),
    1, 2, 50, 'Scheduled'
WHERE NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_title = 'India vs Australia - ODI Demo'
);

INSERT INTO matches
    (match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status)
SELECT
    'Australia vs India - T20 Demo', 'T20', '2026-11-20',
    (SELECT venue_id FROM venues WHERE venue_name = 'Harbour Cricket Ground' LIMIT 1),
    2, 1, 20, 'Scheduled'
WHERE NOT EXISTS (
    SELECT 1 FROM matches
    WHERE match_title = 'Australia vs India - T20 Demo'
);