WITH m AS (
    SELECT "Match".id, "Match".season, "Match".stage, SUBSTR("Match".date, 1, 10) AS match_day,
           home.team_long_name AS home_team, away.team_long_name AS away_team,
           'Home team: ' || home.team_long_name || ', Away team: ' || away.team_long_name
               || ', Date: ' || SUBSTR("Match".date, 1, 10) AS match_key
    FROM "Match"
    INNER JOIN Team AS home ON "Match".home_team_api_id = home.team_api_id
    INNER JOIN Team AS away ON "Match".away_team_api_id = away.team_api_id
    WHERE SUBSTR("Match".date, 1, 7) = '2009-12'
)
SELECT m.home_team, m.away_team, m.match_day
FROM m
WHERE ai_filter('Did the home team win this football match? match_key: ' || m.match_key)
  AND ai_filter('Were more than three goals scored in total in this football match? match_key: ' || m.match_key)
  AND ai_filter('Was this football match played in the England Premier League? match_key: ' || m.match_key)
