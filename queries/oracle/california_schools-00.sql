WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
)
SELECT f."School Name", f."Free Meal Count (Ages 5-17)" / f."Enrollment (Ages 5-17)" AS free_rate
FROM f
WHERE f."Enrollment (K-12)" < 100 AND f."Enrollment (Ages 5-17)" > 0 AND f."Free Meal Count (Ages 5-17)" IS NOT NULL
  AND f."Educational Option Type" = 'Continuation School'
ORDER BY free_rate, f."School Name", f.CDSCode
LIMIT 10
