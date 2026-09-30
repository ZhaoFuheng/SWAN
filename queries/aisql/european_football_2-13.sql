WITH m AS (
    SELECT "Match".id, "Match".season, "Match".stage, SUBSTR("Match".date, 1, 10) AS match_day,
           home.team_long_name AS home_team, away.team_long_name AS away_team,
           'Home team: ' || home.team_long_name || ', Away team: ' || away.team_long_name
               || ', Date: ' || SUBSTR("Match".date, 1, 10) AS match_key
    FROM "Match"
    INNER JOIN Team AS home ON "Match".home_team_api_id = home.team_api_id
    INNER JOIN Team AS away ON "Match".away_team_api_id = away.team_api_id
    WHERE "Match".season = '2015/2016' AND "Match".stage <= 5
)
SELECT COUNT(*)
FROM m
WHERE ai_filter('Was this football match played in the Scotland Premier League? match_key: ' || m.match_key)
