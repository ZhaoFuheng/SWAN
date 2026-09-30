WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT T1."Enrollment (Ages 5-17)"
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE s.EdOpsCode = 'SSS'
  AND s.City = 'Fremont'
  AND T1."Academic Year" = '2014-2015'
