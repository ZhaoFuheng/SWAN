WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
),
ranked AS (
    SELECT DISTINCT substr(s.CDSCode, 1, 14) AS cds, s.School, T1.AvgScrWrite, s.school_address, T1.NumGE1500
    FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
    WHERE T1.NumGE1500 >= 100
)
SELECT ranked.School, ranked.AvgScrWrite, ai_complete('In which city is the school located? school_address: ' || ranked.school_address || ' Answer with the value only, without any other words.') AS City
FROM ranked
ORDER BY ranked.NumGE1500 DESC, ranked.cds
LIMIT 5
