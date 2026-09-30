WITH temp_cte AS (
    SELECT t1.id,
           t1.date,
           t1.season,
           hometeam.team_long_name AS home_team,
           awayteam.team_long_name AS away_team,
           'Home Team: ' || hometeam.team_long_name || ', Away Team: ' || awayteam.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS awayteam ON t1.away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON t1.home_team_api_id = hometeam.team_api_id
    WHERE t1.season = '2015/2016'
),
temp2 AS (
    SELECT *, ai_complete('Provide the league name. match_key: ' || temp_cte.match_key || ' Answer with the value only, without any other words.') AS league_name
    FROM temp_cte
)
SELECT COUNT(temp2.id)
FROM temp2
WHERE temp2.league_name ILIKE '%Scotland Premier League%'
