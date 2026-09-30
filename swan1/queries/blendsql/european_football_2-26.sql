WITH player_key AS (
    SELECT T1.player_name,
           'Player Name: ' || T1.player_name AS player_key
    FROM Player AS T1
),
temp_cte AS (
    SELECT *,
           {{
               LLMMap(
                   'Provide the height in cm.',
                   player_key.player_key
               )
           }} AS height
    FROM player_key
)
SELECT temp_cte.player_name
FROM temp_cte
ORDER BY temp_cte.height ASC
LIMIT 1;
