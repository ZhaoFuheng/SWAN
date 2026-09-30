WITH temp_cte AS (
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS "key"
    FROM Player
),
temp2 AS (
    SELECT any_value(temp_cte.player_name) AS player_name,
           temp_cte.id,
           CAST(SUM(t2.heading_accuracy) AS DOUBLE) / COUNT(t2.player_fifa_api_id) AS heading_accuracy_avg
    FROM temp_cte
    INNER JOIN Player_Attributes AS t2 ON temp_cte.player_api_id = t2.player_api_id
    WHERE ai_filter('Is the player height greater than 180 cm? key: ' || temp_cte."key")
    GROUP BY temp_cte.id
)
SELECT player_name, heading_accuracy_avg
FROM temp2
ORDER BY heading_accuracy_avg DESC, id DESC
LIMIT 10
