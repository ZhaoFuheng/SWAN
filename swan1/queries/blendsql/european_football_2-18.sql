WITH temp_cte AS (
    SELECT t1.date,
           hometeam.team_long_name AS home_team,
           awayteam.team_long_name AS away_team,
           'Home Team: ' || hometeam.team_long_name || ', Away Team: ' || awayteam.team_long_name || ', Date: ' || t1.date AS match_key
    FROM "Match" AS t1
    INNER JOIN Team AS awayteam ON t1.away_team_api_id = awayteam.team_api_id
    INNER JOIN Team AS hometeam ON t1.home_team_api_id = hometeam.team_api_id
),
temp2 AS (
    SELECT temp_cte.match_key,
           {{
               LLMMap(
                   'Provide the league name.',
                   temp_cte.match_key
               )
           }} AS league_name,
           {{
               LLMMap(
                   'Is the match in country Netherlands?',
                   temp_cte.match_key
               )
           }} = TRUE AS in_Netherlands
    FROM temp_cte
)
SELECT temp2.league_name
FROM temp2
GROUP BY temp2.league_name
HAVING in_Netherlands = TRUE
