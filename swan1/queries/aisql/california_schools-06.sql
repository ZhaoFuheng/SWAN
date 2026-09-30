WITH temp_cte AS (
    SELECT T1.Phone, 'Street: ' || T1.Street || ' and School: ' || T1.School AS address
    FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds
    ORDER BY CAST(T2.NumGE1500 AS DOUBLE) / NULLIF(T2.NumTstTakr, 0) DESC
    LIMIT 10
)
SELECT temp_cte.Phone,
    ai_complete('Provide the city name based on the address. address: ' || temp_cte.address || ' Answer with the value only, without any other words.') AS City
FROM temp_cte
