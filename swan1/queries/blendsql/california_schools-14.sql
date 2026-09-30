WITH temp_cte AS (
SELECT frpm.`Enrollment (K-12)`, {{
    LLMMap(
        'Provide the city name based on the address.',
        schools.Street
    )
}} AS City 
FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode
)
SELECT temp_cte.City 
FROM temp_cte 
GROUP BY temp_cte.City
ORDER BY SUM(temp_cte.`Enrollment (K-12)`) ASC 
LIMIT 2
