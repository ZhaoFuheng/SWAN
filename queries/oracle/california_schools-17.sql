WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
),
ranked AS (
    SELECT DISTINCT substr(s.CDSCode, 1, 14) AS cds, s.Street, s.City, s.Zip, s.State, s.school_address, CAST(T1.NumGE1500 AS DOUBLE) / T1.NumTstTakr AS excellence_rate
    FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
    WHERE T1.NumTstTakr >= 100 AND T1.NumGE1500 IS NOT NULL
)
SELECT ranked.Street, ranked.City, ranked.Zip, ranked.State
FROM ranked
ORDER BY ranked.excellence_rate, ranked.cds
LIMIT 10
