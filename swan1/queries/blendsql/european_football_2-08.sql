WITH temp_cte AS (
    SELECT t1.id,
           t1.player_name,
           t1.weight,
           'Player Name: ' || t1.player_name || ', Weight: ' || t1.weight AS player_info_key
    FROM Player AS t1
), 
temp2 AS (
    SELECT temp_cte.id, 
           temp_cte.player_name, 
           temp_cte.weight, 
           {{
               LLMMap(
                   'Is the player__ preferred foot left?',
                   temp_cte.player_info_key
               )
           }} = TRUE AS is_left_foot,
           {{
               LLMMap(
                   'Provide the player birthday (YYYY-MM-DD).',
                   temp_cte.player_info_key
               )
           }} AS birthday
    FROM temp_cte
)
SELECT CAST(COUNT(CASE WHEN temp2.is_left_foot = TRUE THEN temp2.id ELSE NULL END) AS REAL) * 100 / COUNT(temp2.id) AS percent
FROM temp2
WHERE SUBSTR(birthday, 1, 4) BETWEEN '1987' AND '1992'
