WITH temp_cte AS (
    SELECT T1.AvgScrMath, schools.Street
    FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
    ORDER BY T1.NumGE1500 DESC
    LIMIT 1
)
SELECT temp_cte.AvgScrMath,
    ai_complete('Provide the city name based on the address. Street: ' || temp_cte.Street || ' Answer with the value only, without any other words.') AS City
FROM temp_cte
