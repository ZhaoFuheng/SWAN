WITH temp_cte AS (
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS "key"
    FROM Player
),
temp2 AS (
    SELECT id,
           TRY_CAST(ai_complete(
               'Provide the player height (int). key: ' || temp_cte."key" || ' Answer with the number only.'
           ) AS DOUBLE) AS height
    FROM temp_cte
    WHERE ai_filter('Is the player born in between 1990 and 1995? key: ' || temp_cte."key")
)
SELECT SUM(height) / COUNT(id)
FROM temp2
