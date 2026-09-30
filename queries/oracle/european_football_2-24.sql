SELECT Team.team_long_name,
       CASE WHEN ta.buildUpPlaySpeedClass = 'Balanced'
            THEN Team.team_short_name
       END AS team_short_name
FROM Team INNER JOIN Team_Attributes AS ta ON Team.team_api_id = ta.team_api_id
WHERE SUBSTR(ta.date, 1, 4) = '2015'
  AND ta.buildUpPlayPassingClass IN ('Long', 'Short')
