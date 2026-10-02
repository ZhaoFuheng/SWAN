WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT s.School, s.Website AS Website
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.NumTstTakr BETWEEN 150 AND 200
  AND (s.County = 'Los Angeles' OR s.Magnet = 1)
