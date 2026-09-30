WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT f."School Name", s.Street, s.City, s.Zip, s.State
FROM f INNER JOIN s ON f.CDSCode = s.CDSCode
WHERE f."School Type" = 'High Schools (Public)' AND f."FRPM Count (Ages 5-17)" > 800
  AND f."Educational Option Type" = 'Traditional'
  AND NOT f."Charter School (Y/N)" = 1
  AND s.County = 'Monterey'
