WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
)
SELECT f.CDSCode, f."School Name"
FROM f
WHERE f."District Name" = 'Chula Vista Elementary'
  AND ai_filter('Is this a charter school? school_district: ' || f.school_district)
LIMIT 5
