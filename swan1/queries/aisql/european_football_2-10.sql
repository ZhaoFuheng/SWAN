WITH temp_cte AS (
    SELECT t1.id,
           t1.season,
           t1.date,
           t2.team_long_name AS home_team,
           t3.team_long_name AS away_team,
           'Home Team: ' || t2.team_long_name || ', Away Team: ' || t3.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS t2 ON t1.home_team_api_id = t2.team_api_id
    INNER JOIN Team AS t3 ON t1.away_team_api_id = t3.team_api_id
    WHERE t1.season = '2009/2010'
),
temp2 AS (
    SELECT *,
           ai_complete('Provide the league name. match_key: ' || temp_cte.match_key || ' Answer with the value only, without any other words.') AS league_name,
           TRY_CAST(ai_complete(
               'Provide the home team goals. match_key: ' || temp_cte.match_key || ' Answer with the number only.'
           ) AS DOUBLE) AS home_team_goal,
           TRY_CAST(ai_complete(
               'Provide the away team goals. match_key: ' || temp_cte.match_key || ' Answer with the number only.'
           ) AS DOUBLE) AS away_team_goal
    FROM temp_cte
)
SELECT league_name
FROM temp2
GROUP BY league_name
HAVING (CAST(SUM(home_team_goal) AS DOUBLE) / COUNT(DISTINCT temp2.id))
     - (CAST(SUM(away_team_goal) AS DOUBLE) / COUNT(DISTINCT temp2.id)) > 0
