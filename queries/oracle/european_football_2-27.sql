SELECT DISTINCT Team.team_long_name
FROM Team
WHERE SUBSTR(Team.team_short_name, 1, 1) = 'B'
  AND Team.team_api_id IN (SELECT ta.team_api_id FROM Team_Attributes AS ta
                             WHERE SUBSTR(ta.date, 1, 4) = '2012' AND ta.buildUpPlayPassing > 60)
