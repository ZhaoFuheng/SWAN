SELECT ai_agg(list('team_long_name: ' || team_long_name), 'Provide the 3 letters short team name' || ' Answer with the value only, without any other words.')
FROM (
    SELECT Team.team_long_name FROM Team
    WHERE Team.team_long_name = 'Queens Park Rangers'
)
