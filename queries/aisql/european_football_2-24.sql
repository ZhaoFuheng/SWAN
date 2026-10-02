WITH t AS (
    SELECT DISTINCT Team.team_long_name, ta.buildUpPlaySpeedClass
    FROM Team INNER JOIN Team_Attributes AS ta ON Team.team_api_id = ta.team_api_id
    WHERE SUBSTR(ta.date, 1, 4) = '2015'
      AND ta.buildUpPlayPassingClass IN ('Long', 'Short')
)
SELECT t.team_long_name,
       CASE WHEN t.buildUpPlaySpeedClass = 'Balanced'
            THEN ai_complete('What is the three-letter short name of this football team? team_long_name: ' || t.team_long_name || ' Answer with the value only, without any other words.')
       END AS team_short_name
FROM t
