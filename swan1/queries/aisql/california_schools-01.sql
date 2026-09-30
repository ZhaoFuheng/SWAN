WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
)
SELECT T2.Zip
FROM temp_cte AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
WHERE T1."District Name" = 'Fresno County Office of Education'
  AND ai_filter('Is this a charter school? district_school_key: ' || T1.district_school_key)
