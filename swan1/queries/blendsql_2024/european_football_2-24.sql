WITH team_key AS (
    SELECT t1.team_long_name, 'Team Long Name: ' || t1.team_long_name AS team_key
    FROM Team AS t1
    INNER JOIN Team_Attributes AS t2 ON t1.team_api_id = t2.team_api_id
    WHERE t2.buildUpPlaySpeedClass = 'Fast'
),
temp AS (
    SELECT *,
           {{
               LLMMap(
                   'Provide the 3 letters team short name.',
                   'team_key::team_key'
               )
           }} AS team_short_name
    FROM team_key
)
SELECT DISTINCT temp.team_short_name
FROM temp;
