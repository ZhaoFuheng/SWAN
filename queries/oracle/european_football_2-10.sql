WITH m AS (
    SELECT DISTINCT "Match".season, "Match".stage, SUBSTR("Match".date, 1, 10) AS match_day,
           home.team_long_name AS home_team, away.team_long_name AS away_team,
           'Home team: ' || home.team_long_name || ', Away team: ' || away.team_long_name
               || ', Date: ' || SUBSTR("Match".date, 1, 10) AS match_key,
           lg.name AS league_name, ct.name AS country_name,
           "Match".home_team_goal, "Match".away_team_goal
    FROM "Match"
    INNER JOIN Team AS home ON "Match".home_team_api_id = home.team_api_id
    INNER JOIN Team AS away ON "Match".away_team_api_id = away.team_api_id
    INNER JOIN League AS lg ON "Match".league_id = lg.id
    INNER JOIN Country AS ct ON "Match".country_id = ct.id
    WHERE SUBSTR("Match".date, 1, 7) = '2009-12'
)
SELECT m.home_team, m.away_team, m.match_day
FROM m
WHERE m.home_team_goal > m.away_team_goal
  AND m.home_team_goal + m.away_team_goal > 3
  AND m.league_name = 'England Premier League'
