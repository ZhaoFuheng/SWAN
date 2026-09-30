WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
)
SELECT f."School Name", T2.AdmEmail1,
    CASE WHEN f."Enrollment (K-12)" < 300
         THEN CASE WHEN f."Charter School (Y/N)" = 1 THEN 'Yes' ELSE 'No' END END AS is_charter
FROM f INNER JOIN schools AS T2 ON f.CDSCode = T2.CDSCode
WHERE f."District Name" = 'Stockton Unified'
