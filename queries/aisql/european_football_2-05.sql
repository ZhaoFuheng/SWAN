WITH m AS (
    SELECT DISTINCT "Match".season, "Match".stage, SUBSTR("Match".date, 1, 10) AS match_day,
           home.team_long_name AS home_team, away.team_long_name AS away_team,
           'Home team: ' || home.team_long_name || ', Away team: ' || away.team_long_name
               || ', Date: ' || SUBSTR("Match".date, 1, 10) AS match_key
    FROM "Match"
    INNER JOIN Team AS home ON "Match".home_team_api_id = home.team_api_id
    INNER JOIN Team AS away ON "Match".away_team_api_id = away.team_api_id
    WHERE "Match".season = '2009/2010' AND "Match".date >= '2010-01-01'
)
SELECT m.away_team
FROM m
WHERE ai_filter('Context:
[match_key]: «' || m.match_key || '»


Claim: Did the away team win this football match? match_key')
  AND ai_filter('Context:
[match_key]: «' || m.match_key || '»


Claim: Was this football match played in the Scotland Premier League? match_key')
  AND ai_filter('Context:
[match_key]: «' || m.match_key || '»


Claim: Did the away team score at least two goals in this football match? match_key')
GROUP BY m.away_team
ORDER BY COUNT(*) DESC, m.away_team
LIMIT 1
