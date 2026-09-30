WITH temp_cte AS (
    SELECT T1.player_name,
           T1.id,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
)
SELECT DISTINCT id, player_name 
FROM temp_cte
WHERE {{
    LLMMap(
        'Is player preferred foot left',
        temp_cte.player_key
    )
}} = TRUE
