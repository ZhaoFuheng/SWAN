WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.School
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode INNER JOIN f ON f.CDSCode = s.CDSCode
WHERE T1.NumTstTakr > 300
  AND (s.Magnet = 1
       OR (f."Charter School (Y/N)" = 1 AND s.County = 'San Diego'))
