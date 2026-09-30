WITH temp_cte AS (
    SELECT T1.AvgScrMath, schools.Street
    FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
    WHERE T1.AvgScrMath IS NOT NULL
    ORDER BY T1.AvgScrMath + T1.AvgScrRead + T1.AvgScrWrite ASC NULLS FIRST
    LIMIT 1
)
SELECT temp_cte.AvgScrMath,
    ai_complete('Provide the county name based on the street address. Street: ' || temp_cte.Street || ' Answer with the value only, without any other words.') AS County
FROM temp_cte
