WITH temp AS (
    SELECT T1.id,
           T1.player_name,
           T1.weight,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
    WHERE T1.weight < 130
)
SELECT COUNT(DISTINCT id)
FROM temp WHERE {{
    LLMMap(
        'Is the player preferred foot left?',
        'temp::player_key'
    )
}} = TRUE
