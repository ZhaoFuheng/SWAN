WITH temp_cte AS (
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS "key"
    FROM Player
)
SELECT player_name
FROM temp_cte
ORDER BY TRY_CAST(ai_complete(
    'Provide the player height (int). key: ' || temp_cte."key" || ' Answer with the number only.'
) AS DOUBLE) DESC
LIMIT 1
