WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.CDSCode, s.School, s.Website AS Website
FROM s
WHERE s.CDSCode IN (SELECT T1.CDSCode FROM frpm AS T1 WHERE T1."Free Meal Count (Ages 5-17)" BETWEEN 700 AND 1000)
  AND s.County = 'Los Angeles'
LIMIT 5
