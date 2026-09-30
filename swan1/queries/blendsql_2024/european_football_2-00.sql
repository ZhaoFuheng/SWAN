WITH temp AS (
SELECT *, 'Player: '||Player.player_name || ', Player Weight: ' || Player.weight AS key
FROM Player
)
SELECT player_name 
FROM temp
ORDER BY {{
    LLMMap(
        'Provide the player height (int).',
        'temp::key'
    )
}}
DESC LIMIT 1
