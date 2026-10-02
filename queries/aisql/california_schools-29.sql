WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT T1."Enrollment (Ages 5-17)"
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE s.Zip LIKE '945%'
  AND ai_filter('Context:
[school_address]: «' || s.school_address || '»


Claim: Is this a State Special School run by the California Department of Education? school_address')
  AND ai_filter('Context:
[school_address]: «' || s.school_address || '»


Claim: Is the school located in the city of Fremont, California? school_address')
  AND T1."Academic Year" = '2014-2015'
