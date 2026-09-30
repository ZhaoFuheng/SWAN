WITH team_key AS (
    SELECT t1.team_long_name, t2.buildUpPlayPassingClass, 'Team Long Name: ' || t1.team_long_name AS team_key
    FROM Team AS t1
    INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id
    WHERE t2.buildUpPlaySpeedClass = 'Fast'
),
temp_cte AS (
    SELECT *,
           ai_complete('Provide the 3 letters team short name. team_key: ' || team_key.team_key || ' Answer with the value only, without any other words.') AS team_short_name
    FROM team_key
)
SELECT DISTINCT temp_cte.buildUpPlayPassingClass
FROM temp_cte
WHERE temp_cte.team_short_name = 'CLB'
