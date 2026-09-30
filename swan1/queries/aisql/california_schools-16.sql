WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
)
SELECT T2.AdmEmail1
FROM temp_cte AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
WHERE ai_filter('Is this a charter school? district_school_key: ' || T1.district_school_key)
ORDER BY T1."Enrollment (K-12)" ASC NULLS FIRST
LIMIT 1
