USE cricket_stats;

-- ==========================================================
-- REAL INTERNATIONAL CRICKET DATASET
-- Teams, Venues, Marquee Players, Matches & Scorecards
-- ==========================================================

-- 1. Real International Teams
INSERT INTO teams (team_id, team_name, country, team_type) VALUES
(1, 'India', 'India', 'International'),
(2, 'Australia', 'Australia', 'International'),
(3, 'England', 'England', 'International'),
(4, 'South Africa', 'South Africa', 'International'),
(5, 'New Zealand', 'New Zealand', 'International'),
(6, 'Pakistan', 'Pakistan', 'International');

-- 2. Real International Venues
INSERT INTO venues (venue_id, venue_name, city, country) VALUES
(1, 'Wankhede Stadium', 'Mumbai', 'India'),
(2, 'Narendra Modi Stadium', 'Ahmedabad', 'India'),
(3, 'Eden Gardens', 'Kolkata', 'India'),
(4, 'Melbourne Cricket Ground (MCG)', 'Melbourne', 'Australia'),
(5, 'Sydney Cricket Ground (SCG)', 'Sydney', 'Australia'),
(6, 'Lord''s Cricket Ground', 'London', 'England'),
(7, 'Kensington Oval', 'Bridgetown', 'Barbados'),
(8, 'Wanderers Stadium', 'Johannesburg', 'South Africa');

-- 3. Real International Players
INSERT INTO players (player_id, full_name, date_of_birth, nationality, role, batting_style, bowling_style, is_active) VALUES
-- India
(1, 'Rohit Sharma', '1987-04-30', 'India', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(2, 'Virat Kohli', '1988-11-05', 'India', 'Batter', 'Right-hand bat', 'Right-arm medium', 1),
(3, 'Shubman Gill', '1999-09-08', 'India', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(4, 'Rishabh Pant', '1997-10-04', 'India', 'Wicketkeeper', 'Left-hand bat', NULL, 1),
(5, 'Suryakumar Yadav', '1990-09-14', 'India', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(6, 'Hardik Pandya', '1993-10-11', 'India', 'All-rounder', 'Right-hand bat', 'Right-arm fast-medium', 1),
(7, 'Ravindra Jadeja', '1988-12-06', 'India', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
(8, 'Axar Patel', '1994-01-20', 'India', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
(9, 'Jasprit Bumrah', '1993-12-06', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(10, 'Mohammed Shami', '1990-09-03', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(11, 'Kuldeep Yadav', '1994-12-14', 'India', 'Bowler', 'Left-hand bat', 'Left-arm wrist-spin', 1),
(12, 'Arshdeep Singh', '1999-02-05', 'India', 'Bowler', 'Left-hand bat', 'Left-arm medium-fast', 1),
(13, 'KL Rahul', '1992-04-18', 'India', 'Wicketkeeper', 'Right-hand bat', NULL, 1),
(14, 'Shreyas Iyer', '1994-12-06', 'India', 'Batter', 'Right-hand bat', 'Right-arm legbreak', 1),

-- Australia
(15, 'Pat Cummins', '1993-05-08', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(16, 'Travis Head', '1993-12-29', 'Australia', 'Batter', 'Left-hand bat', 'Right-arm offbreak', 1),
(17, 'David Warner', '1986-10-27', 'Australia', 'Batter', 'Left-hand bat', 'Right-arm legbreak', 1),
(18, 'Steve Smith', '1989-06-02', 'Australia', 'Batter', 'Right-hand bat', 'Right-arm legbreak', 1),
(19, 'Marnus Labuschagne', '1994-06-22', 'Australia', 'Batter', 'Right-hand bat', 'Right-arm legbreak', 1),
(20, 'Glenn Maxwell', '1988-10-14', 'Australia', 'All-rounder', 'Right-hand bat', 'Right-arm offbreak', 1),
(21, 'Mitchell Marsh', '1991-10-20', 'Australia', 'All-rounder', 'Right-hand bat', 'Right-arm medium', 1),
(22, 'Alex Carey', '1991-08-27', 'Australia', 'Wicketkeeper', 'Left-hand bat', NULL, 1),
(23, 'Mitchell Starc', '1990-01-30', 'Australia', 'Bowler', 'Left-hand bat', 'Left-arm fast', 1),
(24, 'Josh Hazlewood', '1991-01-08', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast-medium', 1),
(25, 'Adam Zampa', '1992-03-31', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm legbreak', 1),
(26, 'Usman Khawaja', '1986-12-18', 'Australia', 'Batter', 'Left-hand bat', 'Right-arm medium', 1),

-- England
(27, 'Jos Buttler', '1990-09-08', 'England', 'Wicketkeeper', 'Right-hand bat', NULL, 1),
(28, 'Jonny Bairstow', '1989-09-26', 'England', 'Batter', 'Right-hand bat', 'Right-arm medium', 1),
(29, 'Joe Root', '1990-12-30', 'England', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(30, 'Ben Stokes', '1991-06-04', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', 1),
(31, 'Harry Brook', '1999-02-22', 'England', 'Batter', 'Right-hand bat', 'Right-arm medium', 1),
(32, 'Liam Livingstone', '1993-08-04', 'England', 'All-rounder', 'Right-hand bat', 'Right-arm legbreak', 1),
(33, 'Sam Curran', '1998-06-03', 'England', 'All-rounder', 'Left-hand bat', 'Left-arm medium-fast', 1),
(34, 'Jofra Archer', '1995-04-01', 'England', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(35, 'Adil Rashid', '1988-02-17', 'England', 'Bowler', 'Right-hand bat', 'Right-arm legbreak', 1),
(36, 'Mark Wood', '1990-01-11', 'England', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(37, 'Ben Duckett', '1994-10-17', 'England', 'Batter', 'Left-hand bat', 'Right-arm offbreak', 1),

-- South Africa
(38, 'Aiden Markram', '1994-10-04', 'South Africa', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(39, 'Quinton de Kock', '1992-12-17', 'South Africa', 'Wicketkeeper', 'Left-hand bat', NULL, 1),
(40, 'Heinrich Klaasen', '1991-07-30', 'South Africa', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(41, 'David Miller', '1989-06-10', 'South Africa', 'Batter', 'Left-hand bat', 'Right-arm offbreak', 1),
(42, 'Tristan Stubbs', '2000-08-14', 'South Africa', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(43, 'Marco Jansen', '2000-05-01', 'South Africa', 'All-rounder', 'Right-hand bat', 'Left-arm fast', 1),
(44, 'Keshav Maharaj', '1990-02-07', 'South Africa', 'Bowler', 'Right-hand bat', 'Slow left-arm orthodox', 1),
(45, 'Kagiso Rabada', '1995-05-25', 'South Africa', 'Bowler', 'Left-hand bat', 'Right-arm fast', 1),
(46, 'Anrich Nortje', '1993-11-24', 'South Africa', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(47, 'Tabraiz Shamsi', '1990-02-18', 'South Africa', 'Bowler', 'Right-hand bat', 'Left-arm wrist-spin', 1),

-- New Zealand
(48, 'Kane Williamson', '1990-08-08', 'New Zealand', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(49, 'Devon Conway', '1991-07-08', 'New Zealand', 'Wicketkeeper', 'Left-hand bat', 'Right-arm medium', 1),
(50, 'Rachin Ravindra', '1999-11-18', 'New Zealand', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
(51, 'Daryl Mitchell', '1991-05-20', 'New Zealand', 'All-rounder', 'Right-hand bat', 'Right-arm medium', 1),
(52, 'Glenn Phillips', '1996-12-06', 'New Zealand', 'All-rounder', 'Right-hand bat', 'Right-arm offbreak', 1),
(53, 'Mitchell Santner', '1992-02-05', 'New Zealand', 'All-rounder', 'Left-hand bat', 'Slow left-arm orthodox', 1),
(54, 'Trent Boult', '1989-07-22', 'New Zealand', 'Bowler', 'Right-hand bat', 'Left-arm fast-medium', 1),
(55, 'Tim Southee', '1988-12-11', 'New Zealand', 'Bowler', 'Right-hand bat', 'Right-arm medium-fast', 1),
(56, 'Lockie Ferguson', '1991-06-13', 'New Zealand', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),

-- Pakistan
(57, 'Babar Azam', '1994-10-15', 'Pakistan', 'Batter', 'Right-hand bat', 'Right-arm offbreak', 1),
(58, 'Mohammad Rizwan', '1992-06-01', 'Pakistan', 'Wicketkeeper', 'Right-hand bat', 'Right-arm medium', 1),
(59, 'Fakhar Zaman', '1990-04-10', 'Pakistan', 'Batter', 'Left-hand bat', 'Slow left-arm orthodox', 1),
(60, 'Shan Masood', '1989-10-14', 'Pakistan', 'Batter', 'Left-hand bat', 'Right-arm medium-fast', 1),
(61, 'Iftikhar Ahmed', '1990-09-03', 'Pakistan', 'All-rounder', 'Right-hand bat', 'Right-arm offbreak', 1),
(62, 'Shadab Khan', '1998-10-04', 'Pakistan', 'All-rounder', 'Right-hand bat', 'Right-arm legbreak', 1),
(63, 'Shaheen Afridi', '2000-04-06', 'Pakistan', 'Bowler', 'Left-hand bat', 'Left-arm fast', 1),
(64, 'Naseem Shah', '2003-02-15', 'Pakistan', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1),
(65, 'Haris Rauf', '1993-11-07', 'Pakistan', 'Bowler', 'Right-hand bat', 'Right-arm fast', 1);

-- 4. Real Matches
INSERT INTO matches 
(match_id, match_title, format, match_date, venue_id, team1_id, team2_id, overs_limit, status, toss_winner_team_id, toss_decision, winner_team_id, result_type, result_summary, player_of_match_id) VALUES
-- Match 1: ICC T20 World Cup 2024 Final
(1, 'India vs South Africa - ICC Men''s T20 World Cup 2024 Final', 'T20', '2024-06-29', 7, 1, 4, 20, 'Completed', 1, 'Bat', 1, 'Runs', 'India won by 7 runs', 2),

-- Match 2: ICC Cricket World Cup 2023 Final
(2, 'India vs Australia - ICC Cricket World Cup 2023 Final', 'ODI', '2023-11-19', 2, 1, 2, 50, 'Completed', 2, 'Bowl', 2, 'Wickets', 'Australia won by 6 wickets', 16),

-- Match 3: ICC Cricket World Cup 2023 Semi-Final 1
(3, 'India vs New Zealand - ICC Cricket World Cup 2023 Semi-Final', 'ODI', '2023-11-15', 1, 1, 5, 50, 'Completed', 1, 'Bat', 1, 'Runs', 'India won by 70 runs', 10),

-- Match 4: ICC T20 World Cup 2022 Super 12
(4, 'India vs Pakistan - ICC Men''s T20 World Cup 2022 Super 12', 'T20', '2022-10-23', 4, 6, 1, 20, 'Completed', 1, 'Bowl', 1, 'Wickets', 'India won by 4 wickets', 2),

-- Match 5: The Ashes 2023 2nd Test
(5, 'England vs Australia - The Ashes 2023 2nd Test at Lord''s', 'Test', '2023-06-28', 6, 3, 2, NULL, 'Completed', 3, 'Bowl', 2, 'Runs', 'Australia won by 43 runs', 18),

-- Match 6: Upcoming Scheduled Test Clash
(6, 'Australia vs India - Border-Gavaskar Trophy Series', 'Test', '2026-12-05', 4, 2, 1, NULL, 'Scheduled', NULL, NULL, NULL, NULL, 'Upcoming Test clash at the MCG', NULL),

-- Match 7: Upcoming Scheduled ODI Bilateral Series
(7, 'England vs India - 1st ODI Bilateral Series', 'ODI', '2026-11-20', 6, 3, 1, 50, 'Scheduled', NULL, NULL, NULL, NULL, 'Upcoming 3-match ODI series opener at Lord''s', NULL);

-- 5. Match Players (Lineups & Captaincy)
INSERT INTO match_players (match_id, player_id, team_id, playing_xi, captain, wicketkeeper) VALUES
-- Match 1: India vs South Africa (T20 World Cup Final)
(1, 1, 1, 1, 1, 0),
(1, 2, 1, 1, 0, 0),
(1, 4, 1, 1, 0, 1),
(1, 5, 1, 1, 0, 0),
(1, 6, 1, 1, 0, 0),
(1, 7, 1, 1, 0, 0),
(1, 8, 1, 1, 0, 0),
(1, 9, 1, 1, 0, 0),
(1, 11, 1, 1, 0, 0),
(1, 12, 1, 1, 0, 0),
(1, 38, 4, 1, 1, 0),
(1, 39, 4, 1, 0, 1),
(1, 40, 4, 1, 0, 0),
(1, 41, 4, 1, 0, 0),
(1, 42, 4, 1, 0, 0),
(1, 43, 4, 1, 0, 0),
(1, 44, 4, 1, 0, 0),
(1, 45, 4, 1, 0, 0),
(1, 46, 4, 1, 0, 0),

-- Match 2: India vs Australia (CWC 2023 Final)
(2, 1, 1, 1, 1, 0),
(2, 2, 1, 1, 0, 0),
(2, 3, 1, 1, 0, 0),
(2, 5, 1, 1, 0, 0),
(2, 7, 1, 1, 0, 0),
(2, 9, 1, 1, 0, 0),
(2, 10, 1, 1, 0, 0),
(2, 11, 1, 1, 0, 0),
(2, 13, 1, 1, 0, 1),
(2, 14, 1, 1, 0, 0),
(2, 15, 2, 1, 1, 0),
(2, 16, 2, 1, 0, 0),
(2, 17, 2, 1, 0, 0),
(2, 18, 2, 1, 0, 0),
(2, 19, 2, 1, 0, 0),
(2, 20, 2, 1, 0, 0),
(2, 21, 2, 1, 0, 0),
(2, 22, 2, 1, 0, 1),
(2, 23, 2, 1, 0, 0),
(2, 24, 2, 1, 0, 0),
(2, 25, 2, 1, 0, 0),

-- Match 3: India vs New Zealand (CWC 2023 Semi-Final)
(3, 1, 1, 1, 1, 0),
(3, 2, 1, 1, 0, 0),
(3, 3, 1, 1, 0, 0),
(3, 7, 1, 1, 0, 0),
(3, 9, 1, 1, 0, 0),
(3, 10, 1, 1, 0, 0),
(3, 11, 1, 1, 0, 0),
(3, 13, 1, 1, 0, 1),
(3, 14, 1, 1, 0, 0),
(3, 48, 5, 1, 1, 0),
(3, 49, 5, 1, 0, 1),
(3, 50, 5, 1, 0, 0),
(3, 51, 5, 1, 0, 0),
(3, 52, 5, 1, 0, 0),
(3, 53, 5, 1, 0, 0),
(3, 54, 5, 1, 0, 0),
(3, 55, 5, 1, 0, 0),
(3, 56, 5, 1, 0, 0),

-- Match 4: India vs Pakistan (T20 World Cup 2022)
(4, 1, 1, 1, 1, 0),
(4, 2, 1, 1, 0, 0),
(4, 5, 1, 1, 0, 0),
(4, 6, 1, 1, 0, 0),
(4, 8, 1, 1, 0, 0),
(4, 10, 1, 1, 0, 0),
(4, 12, 1, 1, 0, 0),
(4, 13, 1, 1, 0, 1),
(4, 57, 6, 1, 1, 0),
(4, 58, 6, 1, 0, 1),
(4, 60, 6, 1, 0, 0),
(4, 61, 6, 1, 0, 0),
(4, 62, 6, 1, 0, 0),
(4, 63, 6, 1, 0, 0),
(4, 64, 6, 1, 0, 0),
(4, 65, 6, 1, 0, 0),

-- Match 5: England vs Australia (The Ashes 2023 2nd Test)
(5, 15, 2, 1, 1, 0),
(5, 16, 2, 1, 0, 0),
(5, 17, 2, 1, 0, 0),
(5, 18, 2, 1, 0, 0),
(5, 19, 2, 1, 0, 0),
(5, 22, 2, 1, 0, 1),
(5, 23, 2, 1, 0, 0),
(5, 24, 2, 1, 0, 0),
(5, 26, 2, 1, 0, 0),
(5, 27, 3, 1, 0, 0),
(5, 28, 3, 1, 0, 1),
(5, 29, 3, 1, 0, 0),
(5, 30, 3, 1, 1, 0),
(5, 31, 3, 1, 0, 0),
(5, 36, 3, 1, 0, 0),
(5, 37, 3, 1, 0, 0);

-- 6. Match Innings
INSERT INTO innings (innings_id, match_id, innings_number, batting_team_id, total_runs, wickets_lost, legal_balls) VALUES
-- Match 1: India vs South Africa (T20 World Cup 2024 Final)
(1, 1, 1, 1, 176, 7, 120),
(2, 1, 2, 4, 169, 8, 120),

-- Match 2: India vs Australia (CWC 2023 Final)
(3, 2, 1, 1, 240, 10, 300),
(4, 2, 2, 2, 241, 4, 258),

-- Match 3: India vs New Zealand (CWC 2023 Semi-Final)
(5, 3, 1, 1, 397, 4, 300),
(6, 3, 2, 5, 327, 10, 293),

-- Match 4: Pakistan vs India (T20 World Cup 2022)
(7, 4, 1, 6, 159, 8, 120),
(8, 4, 2, 1, 160, 6, 120),

-- Match 5: England vs Australia (The Ashes 2023 2nd Test)
(9, 5, 1, 2, 416, 10, 604),
(10, 5, 2, 3, 325, 10, 458),
(11, 5, 3, 2, 279, 10, 611),
(12, 5, 4, 3, 327, 10, 489);

-- 7. Batting Scorecards
INSERT INTO batting_stats (innings_id, player_id, batting_position, runs, balls_faced, fours, sixes, is_out, dismissal_kind, bowler_player_id) VALUES
-- Match 1 - Innings 1 (India Batting)
(1, 1, 1, 9, 5, 2, 0, 1, 'caught', 44),
(1, 2, 2, 76, 59, 6, 2, 1, 'caught', 43),
(1, 4, 3, 0, 2, 0, 0, 1, 'caught', 44),
(1, 5, 4, 3, 4, 0, 0, 1, 'caught', 45),
(1, 8, 5, 47, 31, 1, 4, 1, 'run out', NULL),
(1, 6, 6, 5, 2, 1, 0, 0, 'not out', NULL),
(1, 7, 7, 2, 2, 0, 0, 1, 'caught', 46),

-- Match 1 - Innings 2 (South Africa Batting)
(2, 39, 1, 39, 31, 4, 1, 1, 'caught', 12),
(2, 38, 2, 4, 5, 0, 0, 1, 'caught', 12),
(2, 42, 3, 31, 21, 3, 1, 1, 'bowled', 8),
(2, 40, 4, 52, 27, 2, 5, 1, 'caught', 6),
(2, 41, 5, 21, 17, 1, 1, 1, 'caught', 6),
(2, 43, 6, 2, 4, 0, 0, 1, 'bowled', 9),
(2, 44, 7, 2, 7, 0, 0, 0, 'not out', NULL),
(2, 45, 8, 4, 3, 1, 0, 1, 'caught', 6),

-- Match 2 - Innings 3 (India Batting vs Australia)
(3, 1, 1, 47, 31, 4, 3, 1, 'caught', 20),
(3, 3, 2, 4, 7, 0, 0, 1, 'caught', 23),
(3, 2, 3, 54, 63, 4, 0, 1, 'bowled', 15),
(3, 14, 4, 4, 3, 1, 0, 1, 'caught', 15),
(3, 13, 5, 66, 107, 1, 0, 1, 'caught', 23),
(3, 7, 6, 9, 22, 0, 0, 1, 'caught', 24),
(3, 5, 7, 18, 28, 1, 0, 1, 'caught', 24),
(3, 10, 8, 6, 10, 1, 0, 1, 'caught', 23),
(3, 9, 9, 1, 3, 0, 0, 1, 'lbw', 25),
(3, 11, 10, 10, 18, 0, 0, 1, 'run out', NULL),

-- Match 2 - Innings 4 (Australia Batting vs India)
(4, 17, 1, 7, 3, 1, 0, 1, 'caught', 10),
(4, 16, 2, 137, 120, 15, 4, 1, 'caught', 9),
(4, 21, 3, 15, 15, 1, 1, 1, 'caught', 9),
(4, 18, 4, 4, 9, 1, 0, 1, 'lbw', 9),
(4, 19, 5, 58, 110, 4, 0, 0, 'not out', NULL),
(4, 20, 6, 2, 1, 0, 0, 0, 'not out', NULL),

-- Match 3 - Innings 5 (India Batting vs New Zealand)
(5, 1, 1, 47, 29, 4, 4, 1, 'caught', 55),
(5, 3, 2, 80, 66, 8, 3, 0, 'retired not out', NULL),
(5, 2, 3, 117, 113, 9, 2, 1, 'caught', 55),
(5, 14, 4, 105, 70, 4, 8, 1, 'caught', 54),
(5, 13, 5, 39, 20, 5, 2, 0, 'not out', NULL),

-- Match 3 - Innings 6 (New Zealand Batting vs India)
(6, 49, 1, 13, 15, 3, 0, 1, 'caught', 10),
(6, 50, 2, 13, 22, 3, 0, 1, 'caught', 10),
(6, 48, 3, 69, 73, 8, 1, 1, 'caught', 10),
(6, 51, 4, 134, 119, 9, 7, 1, 'caught', 10),
(6, 52, 5, 41, 33, 4, 2, 1, 'caught', 9),
(6, 53, 6, 9, 10, 1, 0, 1, 'caught', 10),
(6, 55, 7, 9, 10, 1, 0, 1, 'caught', 10),
(6, 56, 8, 6, 3, 0, 1, 1, 'caught', 10),

-- Match 4 - Innings 7 (Pakistan Batting vs India)
(7, 57, 1, 0, 1, 0, 0, 1, 'lbw', 12),
(7, 58, 2, 4, 12, 1, 0, 1, 'caught', 12),
(7, 60, 3, 52, 42, 5, 0, 0, 'not out', NULL),
(7, 61, 4, 51, 34, 2, 4, 1, 'lbw', 10),
(7, 62, 5, 5, 6, 1, 0, 1, 'caught', 6),
(7, 63, 6, 16, 8, 1, 1, 1, 'bowled', 12),
(7, 65, 7, 6, 4, 0, 1, 0, 'not out', NULL),

-- Match 4 - Innings 8 (India Batting vs Pakistan)
(8, 13, 1, 4, 8, 0, 0, 1, 'bowled', 64),
(8, 1, 2, 4, 7, 0, 0, 1, 'caught', 65),
(8, 2, 3, 82, 53, 6, 4, 0, 'not out', NULL),
(8, 5, 4, 15, 10, 2, 0, 1, 'caught', 65),
(8, 8, 5, 2, 3, 0, 0, 1, 'run out', NULL),
(8, 6, 6, 40, 37, 1, 2, 1, 'caught', 62),

-- Match 5 - Innings 9 (Australia 1st Innings at Lord''s)
(9, 17, 1, 66, 88, 8, 1, 1, 'bowled', 36),
(9, 26, 2, 17, 70, 2, 0, 1, 'bowled', 36),
(9, 19, 3, 47, 93, 7, 0, 1, 'caught', 30),
(9, 18, 4, 110, 184, 15, 0, 1, 'caught', 36),
(9, 16, 5, 77, 73, 14, 0, 1, 'stumped', 29),
(9, 22, 6, 22, 43, 3, 0, 1, 'caught', 29),
(9, 15, 7, 22, 45, 3, 0, 0, 'not out', NULL),

-- Match 5 - Innings 10 (England 1st Innings at Lord''s)
(10, 37, 1, 98, 134, 9, 0, 1, 'caught', 24),
(10, 31, 2, 50, 68, 5, 0, 1, 'caught', 23),
(10, 29, 3, 10, 19, 2, 0, 1, 'caught', 23),
(10, 30, 4, 17, 17, 3, 0, 1, 'caught', 23),
(10, 28, 5, 16, 36, 2, 0, 1, 'bowled', 15),

-- Match 5 - Innings 11 (Australia 2nd Innings at Lord''s)
(11, 26, 1, 77, 187, 12, 0, 1, 'caught', 29),
(11, 18, 2, 34, 62, 4, 0, 1, 'caught', 29),
(11, 16, 3, 7, 16, 1, 0, 1, 'caught', 29),

-- Match 5 - Innings 12 (England 2nd Innings at Lord''s)
(12, 37, 1, 83, 112, 9, 0, 1, 'caught', 24),
(12, 30, 2, 155, 214, 9, 9, 1, 'caught', 24),
(12, 31, 3, 4, 11, 1, 0, 1, 'bowled', 15),
(12, 28, 4, 10, 22, 2, 0, 1, 'stumped', 15);

-- 8. Bowling Scorecards
INSERT INTO bowling_stats (innings_id, player_id, legal_balls, maidens, runs_conceded, wickets, wides, no_balls) VALUES
-- Match 1 - Innings 1 (South Africa Bowling)
(1, 43, 24, 0, 49, 1, 1, 0),
(1, 44, 18, 0, 23, 2, 0, 0),
(1, 45, 24, 0, 36, 1, 1, 0),
(1, 46, 24, 0, 26, 2, 0, 0),

-- Match 1 - Innings 2 (India Bowling)
(2, 12, 24, 0, 20, 2, 0, 0),
(2, 9, 24, 0, 18, 2, 0, 0),
(2, 8, 24, 0, 49, 1, 1, 0),
(2, 11, 24, 0, 45, 0, 0, 0),
(2, 6, 18, 0, 20, 3, 1, 0),

-- Match 2 - Innings 3 (Australia Bowling)
(3, 23, 60, 0, 55, 3, 2, 0),
(3, 24, 60, 0, 60, 2, 1, 0),
(3, 15, 60, 1, 34, 2, 0, 0),
(3, 20, 36, 0, 35, 1, 0, 0),
(3, 25, 60, 0, 44, 1, 1, 0),

-- Match 2 - Innings 4 (India Bowling)
(4, 9, 54, 2, 43, 2, 0, 0),
(4, 10, 42, 1, 47, 1, 1, 0),
(4, 7, 60, 0, 43, 0, 0, 0),
(4, 11, 60, 0, 56, 0, 0, 0),

-- Match 3 - Innings 5 (New Zealand Bowling)
(5, 54, 60, 0, 86, 1, 1, 0),
(5, 55, 60, 0, 100, 3, 2, 0),
(5, 53, 60, 1, 51, 0, 0, 0),
(5, 56, 48, 0, 65, 0, 1, 0),

-- Match 3 - Innings 6 (India Bowling)
(6, 9, 60, 1, 64, 1, 0, 0),
(6, 10, 59, 0, 57, 7, 1, 0),
(6, 7, 60, 0, 63, 0, 0, 0),
(6, 11, 60, 0, 56, 1, 0, 0),

-- Match 4 - Innings 7 (India Bowling vs Pakistan)
(7, 12, 24, 0, 32, 3, 0, 0),
(7, 10, 24, 0, 25, 1, 0, 0),
(7, 6, 24, 0, 30, 3, 1, 0),

-- Match 4 - Innings 8 (Pakistan Bowling vs India)
(8, 64, 24, 0, 23, 1, 0, 0),
(8, 65, 24, 0, 36, 2, 1, 0),
(8, 63, 24, 0, 34, 0, 0, 0),
(8, 62, 24, 0, 38, 1, 0, 0),

-- Match 5 - Innings 9 (England Bowling)
(9, 36, 60, 0, 45, 3, 1, 0),
(9, 30, 72, 1, 21, 1, 0, 0),
(9, 29, 48, 1, 19, 2, 0, 0),

-- Match 5 - Innings 10 (Australia Bowling)
(10, 23, 102, 1, 88, 3, 2, 0),
(10, 24, 78, 0, 71, 2, 0, 0),
(10, 15, 96, 1, 46, 1, 0, 0),

-- Match 5 - Innings 11 (England Bowling)
(11, 29, 90, 1, 40, 3, 0, 0),

-- Match 5 - Innings 12 (Australia Bowling)
(12, 15, 150, 4, 69, 3, 0, 0),
(12, 23, 126, 1, 79, 3, 1, 0),
(12, 24, 102, 2, 80, 3, 0, 0);
