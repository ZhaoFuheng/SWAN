WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
)
SELECT f.CDSCode, f."School Name"
FROM f
WHERE f."District Name" = 'Chula Vista Elementary'
  AND f."Charter School (Y/N)" = 1
LIMIT 5
