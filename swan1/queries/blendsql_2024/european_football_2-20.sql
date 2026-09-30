WITH player_key AS (
    SELECT T1.player_name,
           T1.player_api_id,
           'Player Name: ' || T1.player_name AS player_key
    FROM Player AS T1
),
temp AS (
    SELECT *,
           {{
               LLMMap(
                   'Provide the height in cm.',
                   'player_key::player_key'
               )
           }} AS height
    FROM player_key
)
SELECT A 
FROM (
    SELECT AVG(T3.finishing) AS result, 'Max' AS A 
    FROM Player AS T1
    INNER JOIN Player_Attributes AS T3 ON T1.player_api_id = T3.player_api_id
    WHERE T1.height = (SELECT MAX(height) FROM temp)
    
    UNION

    SELECT AVG(T3.finishing) AS result, 'Min' AS A 
    FROM Player AS T1
    INNER JOIN Player_Attributes AS T3 ON T1.player_api_id = T3.player_api_id
    WHERE T1.height = (SELECT MIN(height) FROM temp)
) AS result_table
ORDER BY result DESC 
LIMIT 1;
