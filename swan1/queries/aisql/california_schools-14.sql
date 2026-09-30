WITH temp_cte AS (
    SELECT frpm."Enrollment (K-12)",
        ai_complete('Provide the city name based on the address. Street: ' || schools.Street || ' Answer with the value only, without any other words.') AS City
    FROM frpm INNER JOIN schools ON frpm.CDSCode = schools.CDSCode
)
SELECT temp_cte.City
FROM temp_cte
GROUP BY temp_cte.City
ORDER BY SUM(temp_cte."Enrollment (K-12)") ASC NULLS FIRST
LIMIT 2
