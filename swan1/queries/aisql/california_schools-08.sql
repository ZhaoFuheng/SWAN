WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
)
SELECT COUNT(T1.CDSCode)
FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds
JOIN temp_cte AS T3 ON T1.CDSCode = T3.CDSCode
WHERE T2.NumTstTakr <= 250
  AND ai_filter('Is the school funded directly under the charter funding type? district_school_key: ' || T3.district_school_key)
  AND ai_filter('Is the address located in Contra Costa County? Street: ' || T1.Street)
