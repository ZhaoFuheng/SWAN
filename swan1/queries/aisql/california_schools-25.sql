WITH temp_cte AS (
    SELECT *,
        ai_complete('Provide the county name based on the street address. Street: ' || schools.Street || ' Answer with the value only, without any other words.') AS County
    FROM schools
    WHERE schools.StatusType = 'Closed'
)
SELECT COUNT(DISTINCT School)
FROM temp_cte
WHERE temp_cte.County = (SELECT T1.County
                         FROM temp_cte AS T1
                         GROUP BY T1.County
                         ORDER BY COUNT(T1.School) DESC
                         LIMIT 1)
  AND temp_cte.StatusType = 'Closed' AND temp_cte.School IS NOT NULL AND temp_cte.Street IS NOT NULL
