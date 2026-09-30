WITH temp AS (
    SELECT T1.player_name,
           T1.weight,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
)
SELECT temp.player_name
FROM temp
WHERE {{
    LLMMap(
        'Is player taller than 180cm?'
        'temp::player_key'
    )
}} = TRUE
