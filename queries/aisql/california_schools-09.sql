WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(T1.CDSCode)
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE T1."Free Meal Count (K-12)" > 500 AND T1."FRPM Count (K-12)" < 700
  AND ai_filter('Is the school located in Los Angeles County, California? school_address: ' || s.school_address)
