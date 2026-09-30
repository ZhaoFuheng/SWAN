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
SELECT ai_classify('Which league does this football team play in? home_team: ' || m.home_team, ['Belgium Jupiler League', 'England Premier League', 'France Ligue 1', 'Germany 1. Bundesliga', 'Italy Serie A', 'Netherlands Eredivisie', 'Poland Ekstraklasa', 'Portugal Liga ZON Sagres', 'Scotland Premier League', 'Spain LIGA BBVA', 'Switzerland Super League']) AS league
FROM m
WHERE ai_filter('Did this football match end in a draw? match_key: ' || m.match_key)
GROUP BY league
ORDER BY COUNT(*) DESC, league
LIMIT 1
