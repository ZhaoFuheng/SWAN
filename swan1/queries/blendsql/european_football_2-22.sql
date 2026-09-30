WITH temp_cte AS (
    SELECT T1.player_name,
           T1.id,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
)
SELECT COUNT(id)
FROM temp_cte
WHERE {{
    LLMMap(
        'Is player born after 1990?',
        temp_cte.player_key
    )
}} = TRUE
