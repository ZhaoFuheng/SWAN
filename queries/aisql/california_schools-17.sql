WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.Street, ai_complete('In which city is the school located? school_address: ' || s.school_address || ' Answer with the value only, without any other words.') AS City, s.Zip, s.State
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.NumTstTakr >= 100 AND T1.NumGE1500 IS NOT NULL
ORDER BY CAST(T1.NumGE1500 AS DOUBLE) / T1.NumTstTakr, s.CDSCode
LIMIT 10
