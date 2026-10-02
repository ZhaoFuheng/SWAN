WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
),
high_math AS (
    SELECT DISTINCT substr(s.CDSCode, 1, 14) AS cds, T1.AvgScrMath, s.County AS County
    FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
    WHERE T1.AvgScrMath >= 550
)
SELECT a.County, AVG(a.AvgScrMath)
FROM high_math AS a
WHERE a.County = (SELECT b.County FROM high_math AS b GROUP BY b.County ORDER BY COUNT(*) DESC, b.County LIMIT 1)
GROUP BY a.County
