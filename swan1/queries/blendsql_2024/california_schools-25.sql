WITH temp AS (
SELECT *, {{
    LLMMap(
        'Provide the county name based on the street address.',
        'schools::Street'
    )
}} AS County
FROM schools
WHERE schools.StatusType = 'Closed' 
)
SELECT COUNT(DISTINCT School)
FROM temp
WHERE temp.County = ( SELECT T1.County 
                     FROM temp AS T1 
                     GROUP BY T1.County ORDER BY COUNT(T1.School) DESC LIMIT 1 
                   ) 
AND temp.StatusType = 'Closed' AND temp.school IS NOT NULL AND temp.Street IS NOT NULL
