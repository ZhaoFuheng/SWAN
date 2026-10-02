SELECT DISTINCT Team.team_long_name
FROM Team
WHERE ai_filter('Context:
[team_long_name]: «' || Team.team_long_name || '»


Claim: Does the three-letter short name of this football team start with the letter L? team_long_name')
  AND Team.team_api_id IN (SELECT ta.team_api_id FROM Team_Attributes AS ta
                             WHERE SUBSTR(ta.date, 1, 4) = '2015' AND ta.chanceCreationPassingClass = 'Risky')
