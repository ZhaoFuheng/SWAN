SELECT DISTINCT ta.buildUpPlayPassingClass
FROM Team INNER JOIN Team_Attributes AS ta ON Team.team_api_id = ta.team_api_id
WHERE ai_filter('Context:
[team_long_name]: «' || Team.team_long_name || '»


Claim: Is CLB the three-letter short name of this football team? team_long_name')
  AND SUBSTR(ta.date, 1, 4) = '2015'
