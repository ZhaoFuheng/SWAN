WITH temp AS (
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
    SELECT *, {{
        LLMMap(
            'Provide the league name.',
            'temp::match_key'
        )
    }} AS league_name
    FROM temp
)
SELECT COUNT(temp2.id)
FROM temp2
WHERE temp2.league_name LIKE '%Scotland Premier League%'
