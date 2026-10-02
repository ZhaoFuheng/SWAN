WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(DISTINCT substr(T1.CDSCode, 1, 14))
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE T1."Free Meal Count (K-12)" > 500 AND T1."FRPM Count (K-12)" < 700
  AND s.County = 'Los Angeles'
