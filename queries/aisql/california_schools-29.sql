WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT T1."Enrollment (Ages 5-17)"
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE s.EdOpsCode = 'SSS'
  AND ai_filter('Is the school located in the city of Fremont, California? school_address: ' || s.school_address)
  AND T1."Academic Year" = '2014-2015'
