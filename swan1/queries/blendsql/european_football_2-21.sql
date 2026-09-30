WITH temp_cte AS (
    SELECT T1.player_name,
           T1.weight,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
)
SELECT temp_cte.player_name
FROM temp_cte
WHERE {{
    LLMMap(
        'Is player taller than 180cm?',
        temp_cte.player_key
    )
}} = TRUE
