WITH temp_cte AS (
    SELECT *, 'Player: ' || Player.player_name || ', Player Weight: ' || Player.weight AS "key"
    FROM Player
),
temp2 AS (
    SELECT t2.id, t2.overall_rating,
           TRY_CAST(ai_complete(
               'Provide the player height (int). key: ' || temp_cte."key" || ' Answer with the number only.'
           ) AS DOUBLE) AS height
    FROM temp_cte INNER JOIN Player_Attributes AS t2 ON temp_cte.player_api_id = t2.player_api_id
    WHERE SUBSTR(t2.date, 1, 4) BETWEEN '2010' AND '2015'
)
SELECT CAST(SUM(temp2.overall_rating) AS DOUBLE) / COUNT(temp2.id)
FROM temp2
WHERE temp2.height > 179
