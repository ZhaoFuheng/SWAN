WITH temp_cte AS (
SELECT *, {{
    LLMMap(
        'Provide the county name based on the street address.',
        schools.Street
    )
}} AS County
FROM schools
WHERE schools.StatusType = 'Closed' 
)
SELECT COUNT(DISTINCT School)
FROM temp_cte
WHERE temp_cte.County = ( SELECT T1.County 
                     FROM temp_cte AS T1 
                     GROUP BY T1.County ORDER BY COUNT(T1.School) DESC LIMIT 1 
                   ) 
AND temp_cte.StatusType = 'Closed' AND temp_cte.school IS NOT NULL AND temp_cte.Street IS NOT NULL
