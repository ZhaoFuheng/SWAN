WITH temp_cte AS (
    SELECT *, year||' '||name AS key
    FROM races
)
SELECT CAST(COUNT(CASE WHEN T2.time IS NOT NULL THEN T2.driverId END) AS REAL) * 100 / COUNT(T2.driverId)
FROM temp_cte INNER JOIN results AS T2 ON T2.raceId = temp_cte.raceId
WHERE temp_cte.year = 1983 AND {{
    LLMMap(
        'Was the race on 07-16?',
        temp_cte.key
    )
}} = TRUE
