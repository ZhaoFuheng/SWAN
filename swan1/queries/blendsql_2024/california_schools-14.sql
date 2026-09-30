WITH temp AS (
SELECT frpm.`Enrollment (K-12)`, {{
    LLMMap(
        'Provide the city name based on the address.',
        'schools::Street'
    )
}} AS City 
FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode
)
SELECT temp.City 
FROM temp 
GROUP BY temp.City
ORDER BY SUM(temp.`Enrollment (K-12)`) ASC 
LIMIT 2
