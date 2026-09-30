WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.School, T1.AvgScrWrite, s.City AS City
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.NumGE1500 >= 100
ORDER BY T1.NumGE1500 DESC, s.CDSCode
LIMIT 5
