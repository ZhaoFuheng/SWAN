WITH temp_cte AS (
SELECT *, 'Player: '||Player.player_name || ', Player Weight: ' || Player.weight AS key
FROM Player
), 
temp2 AS (
SELECT id, {{
    LLMMap(
        'Provide the player height (int).',
        temp_cte.key
    )
}} AS height
FROM temp_cte
WHERE {{
    LLMMap(
        'Is the player born in between 1990 and 1995?',
        temp_cte.key
    )
}} = TRUE
)
SELECT SUM(height) / COUNT(id)
FROM temp2
