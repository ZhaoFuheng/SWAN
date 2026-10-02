WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
)
SELECT DISTINCT substr(f.CDSCode, 1, 14) AS CDSCode, f."School Name"
FROM f
WHERE f."District Name" = 'Chula Vista Elementary'
  AND ai_filter('Context:
[school_district]: «' || f.school_district || '»


Claim: Is this a charter school? school_district')
LIMIT 5
