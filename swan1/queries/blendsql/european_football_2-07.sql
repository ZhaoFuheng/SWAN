WITH temp_cte AS (
    SELECT t1.id, 
           hometeam.team_long_name AS home_team, 
           awayteam.team_long_name AS away_team, 
           t1.date,
           'Home Team: ' || hometeam.team_long_name || ', Away Team: ' || awayteam.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS awayteam ON t1.away_team_api_id = awayteam.team_api_id 
    INNER JOIN Team AS hometeam ON t1.home_team_api_id = hometeam.team_api_id
),
temp2 AS (
    SELECT *, {{
        LLMMap(
            'Provide the football league name.',
            temp_cte.match_key
        )
    }} AS league_name
    FROM temp_cte
)
SELECT league_name, COUNT(id)
FROM temp2
GROUP BY league_name
ORDER BY COUNT(id) DESC
LIMIT 1;
