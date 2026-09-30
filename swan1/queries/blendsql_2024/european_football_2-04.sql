WITH temp AS (
    SELECT t1.date, t2.team_long_name AS home_team, t3.team_long_name AS away_team,
           'Home Team: ' || t2.team_long_name || ', Away Team: ' || t3.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS t2 ON t1.home_team_api_id = t2.team_api_id
    INNER JOIN Team AS t3 ON t1.away_team_api_id = t3.team_api_id
    WHERE t1.season = '2015/2016'
), 
temp2 AS (
    SELECT temp.*, {{
        LLMMap(
            'Provide the league name.',
            'temp::match_key'
        )
    }} AS league_name,
    {{
        LLMMap(
            'Provide the total goals for this match.',
            'temp::match_key'
        )
    }} AS total_goals
    FROM temp
)
SELECT league_name 
FROM temp2
GROUP BY league_name
ORDER BY SUM(total_goals) DESC
LIMIT 1;
