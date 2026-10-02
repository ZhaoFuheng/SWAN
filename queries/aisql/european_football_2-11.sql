SELECT DISTINCT ai_complete('What is the three-letter short name of this football team? team_long_name: ' || Team.team_long_name || ' Answer with the value only, without any other words.') AS team_short_name
FROM Team
WHERE Team.team_long_name = 'Queens Park Rangers'
