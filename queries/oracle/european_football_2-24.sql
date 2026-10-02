WITH t AS (
    SELECT DISTINCT Team.team_long_name, Team.team_short_name, ta.buildUpPlaySpeedClass
    FROM Team INNER JOIN Team_Attributes AS ta ON Team.team_api_id = ta.team_api_id
    WHERE SUBSTR(ta.date, 1, 4) = '2015'
      AND ta.buildUpPlayPassingClass IN ('Long', 'Short')
)
SELECT t.team_long_name,
       CASE WHEN t.buildUpPlaySpeedClass = 'Balanced'
            THEN t.team_short_name
       END AS team_short_name
FROM t
