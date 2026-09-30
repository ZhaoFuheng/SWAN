WITH temp AS (
SELECT t1.player_api_id, t2.player_name, t1.sprint_speed, t1.`date`
FROM Player_Attributes AS t1 INNER JOIN Player AS t2 ON t1.player_api_id = t2.player_api_id
WHERE SUBSTR(t1.`date`, 1, 10) BETWEEN '2013-01-01' AND '2015-12-31' AND t1.sprint_speed >= 97
), 
temp2 AS (
    SELECT temp.*, {{
        LLMMap(
            'Provide the birthday for this player (in SQL Datetime format).',
            'temp::player_name'
        )
    }} AS birthday
    FROM temp
)
SELECT DATETIME('now') - birthday AS age
FROM temp2;
