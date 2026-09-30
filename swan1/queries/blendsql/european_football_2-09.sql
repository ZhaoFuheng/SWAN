WITH temp_cte AS (
    SELECT t1.id,
           t1.date,
           t2.team_long_name AS home_team,
           t3.team_long_name AS away_team,
           'Home Team: ' || t2.team_long_name || ', Away Team: ' || t3.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS t2 ON t1.home_team_api_id = t2.team_api_id
    INNER JOIN Team AS t3 ON t1.away_team_api_id = t3.team_api_id
),
temp2 AS (
    SELECT *, 
           {{
               LLMMap(
                   'Provide the league name.',
                   temp_cte.match_key
               )
           }} AS league_name,
           {{
               LLMMap(
                   'Provide the home team goals.',
                   temp_cte.match_key
               )
           }} AS home_team_goal,
           {{
               LLMMap(
                   'Provide the away team goals.',
                   temp_cte.match_key
               )
           }} AS away_team_goal
    FROM temp_cte
)
SELECT league_name, SUM(home_team_goal) + SUM(away_team_goal) AS total_goals
FROM temp2
GROUP BY league_name
ORDER BY total_goals ASC
LIMIT 5;
