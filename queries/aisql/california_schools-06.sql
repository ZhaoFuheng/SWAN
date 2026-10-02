WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
),
ranked AS (
    SELECT DISTINCT substr(s.CDSCode, 1, 14) AS cds, s.Phone, s.school_address, CAST(T1.NumGE1500 AS DOUBLE) / T1.NumTstTakr AS excellence_rate
    FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
    WHERE T1.NumTstTakr >= 100 AND T1.NumGE1500 IS NOT NULL
)
SELECT ranked.Phone, ai_complete('In which city is the school located? school_address: ' || ranked.school_address || ' Answer with the value only, without any other words.') AS City
FROM ranked
ORDER BY ranked.excellence_rate DESC, ranked.cds
LIMIT 10
