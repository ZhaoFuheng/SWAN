WITH temp_cte AS (
    SELECT schools.Street, schools.Zip, schools.State
    FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
    ORDER BY CAST(T1.NumGE1500 AS DOUBLE) / NULLIF(T1.NumTstTakr, 0) ASC NULLS FIRST
    LIMIT 10
)
SELECT temp_cte.Street,
    ai_complete('Provide the city name based on the address. Street: ' || temp_cte.Street || ' Answer with the value only, without any other words.') AS City,
    temp_cte.Zip, temp_cte.State
FROM temp_cte
