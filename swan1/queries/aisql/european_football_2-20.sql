WITH player_key AS (
    SELECT T1.player_name,
           T1.player_api_id,
           'Player Name: ' || T1.player_name AS player_key
    FROM Player AS T1
),
temp_cte AS MATERIALIZED (
    SELECT *,
           TRY_CAST(ai_complete(
               'Provide the height in cm. player_key: ' || player_key.player_key || ' Answer with the number only.'
           ) AS DOUBLE) AS height
    FROM player_key
)
SELECT A
FROM (
    SELECT AVG(T3.finishing) AS result, 'Max' AS A
    FROM temp_cte
    INNER JOIN Player_Attributes AS T3 ON temp_cte.player_api_id = T3.player_api_id
    WHERE temp_cte.height = (SELECT MAX(height) FROM temp_cte)

    UNION

    SELECT AVG(T3.finishing) AS result, 'Min' AS A
    FROM temp_cte
    INNER JOIN Player_Attributes AS T3 ON temp_cte.player_api_id = T3.player_api_id
    WHERE temp_cte.height = (SELECT MIN(height) FROM temp_cte)
) AS result_table
ORDER BY result DESC
LIMIT 1
