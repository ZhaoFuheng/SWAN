WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
local_k12 AS (
    SELECT f."Enrollment (K-12)" AS enroll_k12, f."Enrollment (Ages 5-17)" AS enroll_5_17
    FROM f
    WHERE f."School Type" = 'K-12 Schools (Public)'
      AND ai_filter('Is this school a locally funded charter school? school_district: ' || f.school_district)
)
SELECT COUNT(*)
FROM local_k12 AS a
WHERE a.enroll_k12 - a.enroll_5_17 > (SELECT AVG(b.enroll_k12 - b.enroll_5_17) FROM local_k12 AS b)
