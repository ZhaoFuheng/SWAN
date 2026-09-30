WITH temp_cte AS (
SELECT *, 'Player: '||Player.player_name || ', Player Weight: ' || Player.weight AS key
FROM Player
)
SELECT player_name 
FROM temp_cte
ORDER BY {{
    LLMMap(
        'Provide the player height (int).',
        temp_cte.key
    )
}}
DESC LIMIT 1
