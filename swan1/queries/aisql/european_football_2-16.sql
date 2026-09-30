WITH temp_cte AS (
    SELECT t1.team_long_name,
           'Team Long Name: ' || t1.team_long_name AS team_key
    FROM Team AS t1
    INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id
    WHERE t2.chanceCreationPassingClass = 'Risky'
),
temp2 AS (
    SELECT temp_cte.team_long_name,
           ai_complete('Provide the team short name (3 letters code). team_key: ' || temp_cte.team_key || ' Answer with the value only, without any other words.') AS team_short_name
    FROM temp_cte
)
SELECT DISTINCT temp2.team_short_name
FROM temp2
