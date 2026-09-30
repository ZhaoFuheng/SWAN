WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
)
SELECT T2.Phone
FROM temp_cte AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
WHERE T2.OpenDate > '2000-01-01'
  AND ai_filter('Is this a charter school? district_school_key: ' || T1.district_school_key)
  AND ai_filter('Is the school funded directly under the charter funding type? district_school_key: ' || T1.district_school_key)
