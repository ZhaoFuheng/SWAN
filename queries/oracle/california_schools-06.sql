WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.Phone, s.City
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.NumTstTakr >= 100 AND T1.NumGE1500 IS NOT NULL
ORDER BY CAST(T1.NumGE1500 AS DOUBLE) / T1.NumTstTakr DESC, s.CDSCode
LIMIT 10
