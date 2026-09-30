WITH temp AS (
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS key
    FROM Player
), 
temp2 AS (
    SELECT temp.player_name, 
           temp.id,
           CAST(SUM(t2.heading_accuracy) AS REAL) / COUNT(t2.`player_fifa_api_id`) AS heading_accuracy_avg
    FROM temp
    INNER JOIN Player_Attributes AS t2 ON temp.player_api_id = t2.player_api_id 
    WHERE {{
        LLMMap(
            'Is the player height greater than 180 cm?',
            'temp::key'
        )
    }} = TRUE
    GROUP BY temp.id
)
SELECT player_name, heading_accuracy_avg
FROM temp2
ORDER BY heading_accuracy_avg DESC, id DESC
LIMIT 10;
