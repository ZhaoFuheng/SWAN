WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(*)
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode INNER JOIN f ON f.CDSCode = s.CDSCode
WHERE T1.AvgScrMath > 560
  AND f."Charter School (Y/N)" = 1
  AND f."Charter Funding Type" = 'Directly funded'
  AND NOT s.Magnet = 1
