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
    WHERE t1.season = '2010/2011'
),
temp2 AS (
    SELECT temp_cte.match_key,
           temp_cte.id,
           TRY_CAST(ai_complete(
               'Provide the home team goals. match_key: ' || temp_cte.match_key || ' Answer with the number only.'
           ) AS DOUBLE) AS home_team_goal,
           ai_filter('Is the match in country Poland. match_key: ' || temp_cte.match_key) AS in_Poland
    FROM temp_cte
)
SELECT CAST(SUM(temp2.home_team_goal) AS DOUBLE) / COUNT(temp2.id) AS avg_home_goals
FROM temp2
WHERE temp2.in_Poland
