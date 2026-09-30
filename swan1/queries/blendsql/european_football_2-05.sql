WITH temp_cte AS (
    SELECT t1.date, 
           away.team_long_name AS away_team, 
           home.team_long_name AS home_team,
           'Home Team: ' || home.team_long_name || ', Away Team: ' || away.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS away ON t1.away_team_api_id = away.team_api_id
    INNER JOIN Team AS home ON t1.home_team_api_id = home.team_api_id
    WHERE t1.season = '2009/2010'
), 
temp2 AS (
    SELECT temp_cte.away_team, {{
        LLMMap(
            'Provide the league name for this match.',
            temp_cte.match_key
        )
    }} AS league_name,
    {{
        LLMMap(
            'Provide the goals for home and away teams in this match.',
            temp_cte.match_key
        )
    }} AS goal_difference
    FROM temp_cte
)
SELECT away_team
FROM temp2
WHERE league_name = 'Scotland Premier League'
  AND goal_difference > 0
GROUP BY away_team
ORDER BY COUNT(*) DESC
LIMIT 1;
