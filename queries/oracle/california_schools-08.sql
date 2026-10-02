WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(DISTINCT substr(s.CDSCode, 1, 14))
FROM s INNER JOIN satscores AS T2 ON s.CDSCode = T2.cds INNER JOIN f ON s.CDSCode = f.CDSCode
WHERE T2.NumTstTakr BETWEEN 100 AND 250
  AND NOT s.Magnet = 1
  AND f."Charter School (Y/N)" = 1
  AND f."Charter Funding Type" = 'Directly funded'
  AND s.County = 'Los Angeles'
