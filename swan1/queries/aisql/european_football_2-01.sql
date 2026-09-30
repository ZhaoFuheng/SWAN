WITH temp_cte AS (
    SELECT "Match".id,
           'Hometeam: ' || hometeam.team_long_name || ', Awayteam: ' || awayteam.team_long_name AS teamnames,
           'Hometeam: ' || hometeam.team_long_name || ', Awayteam: ' || awayteam.team_long_name
               || ', Date: ' || "Match".date AS match_key
    FROM "Match"
    INNER JOIN Team AS awayteam ON "Match".away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON "Match".home_team_api_id = hometeam.team_api_id
    WHERE "Match".season = '2015/2016'
),
temp2 AS (
    SELECT temp_cte.id,
           ai_complete('Provide the football league name. teamnames: ' || temp_cte.teamnames || ' Answer with the value only, without any other words.') AS league_name
    FROM temp_cte
    WHERE ai_filter('Did the match end in a draw? match_key: ' || temp_cte.match_key)
)
SELECT temp2.league_name
FROM temp2
GROUP BY temp2.league_name
ORDER BY COUNT(temp2.id) DESC
LIMIT 1
