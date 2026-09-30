WITH temp_cte AS (
    SELECT t1.player_api_id, t2.player_name, t1.sprint_speed, t1.date
    FROM Player_Attributes AS t1
    INNER JOIN Player AS t2 ON t1.player_api_id = t2.player_api_id
    WHERE SUBSTR(t1.date, 1, 10) BETWEEN '2013-01-01' AND '2015-12-31' AND t1.sprint_speed >= 97
),
temp2 AS (
    SELECT *,
           TRY_CAST(ai_complete(
               'Provide the birthday for this player (in SQL Datetime format). player_name: ' || temp_cte.player_name
               || ' Answer with the date only, in YYYY-MM-DD format.'
           ) AS DATE) AS birthday
    FROM temp_cte
)
-- sqlite's DATETIME('now') - birthday subtracts the leading numbers of the two texts: the years
SELECT year(CAST(get_current_timestamp() AS TIMESTAMP)) - year(birthday) AS age
FROM temp2
