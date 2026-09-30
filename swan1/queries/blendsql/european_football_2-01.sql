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
    SELECT temp_cte.id, {{
        LLMMap(
            'Provide the football league name.',
            temp_cte.teamnames
        )
    }} AS league_name
    FROM temp_cte
    WHERE {{
        LLMMap(
            'Did the match end in a draw?',
            temp_cte.match_key
        )
    }} = TRUE
)
SELECT temp2.league_name
FROM temp2
GROUP BY temp2.league_name
ORDER BY COUNT(temp2.id) DESC LIMIT 1
