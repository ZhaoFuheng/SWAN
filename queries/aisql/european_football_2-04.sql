WITH m AS (
    SELECT "Match".id, "Match".season, "Match".stage, SUBSTR("Match".date, 1, 10) AS match_day,
           home.team_long_name AS home_team, away.team_long_name AS away_team,
           'Home team: ' || home.team_long_name || ', Away team: ' || away.team_long_name
               || ', Date: ' || SUBSTR("Match".date, 1, 10) AS match_key
    FROM "Match"
    INNER JOIN Team AS home ON "Match".home_team_api_id = home.team_api_id
    INNER JOIN Team AS away ON "Match".away_team_api_id = away.team_api_id
    WHERE "Match".season = '2015/2016' AND "Match".stage <= 3
),
g AS (
    SELECT ai_classify('Which league was this football match played in? match_key: ' || m.match_key, ['Belgium Jupiler League', 'England Premier League', 'France Ligue 1', 'Germany 1. Bundesliga', 'Italy Serie A', 'Netherlands Eredivisie', 'Poland Ekstraklasa', 'Portugal Liga ZON Sagres', 'Scotland Premier League', 'Spain LIGA BBVA', 'Switzerland Super League']) AS league,
           TRY_CAST(ai_complete('How many goals were scored in total in this football match? match_key: ' || m.match_key
                                || ' Answer with the number only.') AS DOUBLE) AS goals
    FROM m
)
SELECT g.league
FROM g
GROUP BY g.league
ORDER BY SUM(g.goals) DESC, g.league
LIMIT 1
