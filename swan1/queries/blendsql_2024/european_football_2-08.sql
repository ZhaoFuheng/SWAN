WITH temp AS (
    SELECT t1.id,
           t1.player_name,
           t1.weight,
           'Player Name: ' || t1.player_name || ', Weight: ' || t1.weight AS player_info_key
    FROM Player AS t1
), 
temp2 AS (
    SELECT temp.id, 
           temp.player_name, 
           temp.weight, 
           {{
               LLMMap(
                   'Is the player__ preferred foot left?',
                   'temp::player_info_key'
               )
           }} AS is_left_foot,
           {{
               LLMMap(
                   'Provide the player birthday (YYYY-MM-DD).',
                   'temp::player_info_key'
               )
           }} AS birthday
    FROM temp
)
SELECT CAST(COUNT(CASE WHEN temp2.is_left_foot = 't' THEN temp2.id ELSE NULL END) AS REAL) * 100 / COUNT(temp2.id) AS percent
FROM temp2
WHERE SUBSTR(birthday, 1, 4) BETWEEN '1987' AND '1992'
