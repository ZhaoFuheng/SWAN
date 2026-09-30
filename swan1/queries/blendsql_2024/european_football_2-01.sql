WITH temp AS (
SELECT "Match".id, CONCAT("Hometeam: ", hometeam.team_long_name, ", Awayteam: ", awayteam.team_long_name) AS teamnames
FROM "Match"
INNER JOIN Team AS awayteam ON "Match".away_team_api_id = awayteam.team_api_id 
INNER JOIN Team AS hometeam ON "Match".home_team_api_id = hometeam.team_api_id 
WHERE "Match".season = '2015/2016' AND "Match".home_team_goal = "Match".away_team_goal
), 
temp2 AS (
    SELECT temp.id, {{
        LLMMap(
            'Provide the football league name.',
            'temp::teamnames'
        )
    }} AS league_name
    FROM temp
)
SELECT temp2.league_name 
FROM temp2
GROUP BY temp2.league_name
ORDER BY COUNT(temp2.id) DESC LIMIT 1;
