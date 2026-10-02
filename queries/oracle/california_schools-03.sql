WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT s.School, s.Phone
FROM f INNER JOIN s ON f.CDSCode = s.CDSCode
WHERE s.OpenDate > '2012-01-01'
  AND f."Charter School (Y/N)" = 1
  AND f."Charter Funding Type" = 'Directly funded'
  AND s.County = 'Fresno'
