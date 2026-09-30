WITH temp_cte AS (
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS key
    FROM Player
),
temp2 AS (
    SELECT t2.id, t2.overall_rating, {{
        LLMMap(
            'Provide the player height (int).',
            temp_cte.key
        )
    }} AS height
    FROM temp_cte INNER JOIN Player_Attributes AS t2 ON temp_cte.player_api_id = t2.player_api_id
    WHERE SUBSTR(t2.`date`, 1, 4) BETWEEN '2010' AND '2015'
)
SELECT CAST(SUM(temp2.overall_rating) AS REAL) / COUNT(temp2.id)
FROM temp2
WHERE temp2.height > 179
