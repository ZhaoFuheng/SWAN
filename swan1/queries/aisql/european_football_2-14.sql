WITH temp_cte AS (
    SELECT T1.player_name,
           T1.weight,
           'Player Name: ' || T1.player_name || ', Weight: ' || T1.weight AS player_key
    FROM Player AS T1
),
temp2 AS (
    SELECT temp_cte.player_name,
           temp_cte.player_key,
           ai_complete('Provide the preferred foot (left or right). player_key: ' || temp_cte.player_key || ' Answer with the value only, without any other words.') AS preferred_foot,
           TRY_CAST(ai_complete(
               'Provide the player__ birthday (YYYY-MM-DD). player_key: ' || temp_cte.player_key
               || ' Answer with the date only, in YYYY-MM-DD format.'
           ) AS DATE) AS birthday
    FROM temp_cte
)
SELECT temp2.preferred_foot
FROM temp2
ORDER BY temp2.birthday DESC
LIMIT 1
