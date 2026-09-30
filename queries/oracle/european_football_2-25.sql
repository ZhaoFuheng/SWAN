SELECT DISTINCT ta.buildUpPlayPassingClass
FROM Team INNER JOIN Team_Attributes AS ta ON Team.team_api_id = ta.team_api_id
WHERE Team.team_short_name = 'CLB'
  AND SUBSTR(ta.date, 1, 4) = '2015'
