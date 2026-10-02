WITH m AS (
    SELECT DISTINCT "Match".season, "Match".stage, SUBSTR("Match".date, 1, 10) AS match_day,
           home.team_long_name AS home_team, away.team_long_name AS away_team,
           'Home team: ' || home.team_long_name || ', Away team: ' || away.team_long_name
               || ', Date: ' || SUBSTR("Match".date, 1, 10) AS match_key
    FROM "Match"
    INNER JOIN Team AS home ON "Match".home_team_api_id = home.team_api_id
    INNER JOIN Team AS away ON "Match".away_team_api_id = away.team_api_id
    WHERE "Match".season = '2010/2011' AND "Match".stage <= 15
)
SELECT AVG(TRY_CAST(ai_complete('How many goals did the home team score in this football match? match_key: ' || m.match_key
                                || ' Answer with the number only.') AS DOUBLE)) AS avg_home_goals
FROM m
WHERE ai_filter('Context:
[home_team]: «' || m.home_team || '»


Claim: Is this football team based in Poland? home_team')
