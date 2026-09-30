WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.CDSCode, s.School, ai_complete('What is the website address of the school? school_address: ' || s.school_address || ' Answer with the value only, without any other words.') AS Website
FROM s
WHERE s.CDSCode IN (SELECT T1.CDSCode FROM frpm AS T1 WHERE T1."Free Meal Count (Ages 5-17)" BETWEEN 700 AND 1000)
  AND ai_filter('Is the school located in Los Angeles County, California? school_address: ' || s.school_address)
LIMIT 5
