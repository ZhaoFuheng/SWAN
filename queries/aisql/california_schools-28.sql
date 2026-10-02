WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT substr(s.CDSCode, 1, 14) AS CDSCode, s.School
FROM s
WHERE (s.Zip LIKE '952%' OR s.Zip LIKE '953%')
  AND ai_filter('Context:
[school_address]: «' || s.school_address || '»


Claim: Is this a continuation high school? school_address')
  AND s.StatusType = 'Active' AND s.MailState = 'CA'
  AND ai_filter('Context:
[school_address]: «' || s.school_address || '»


Claim: Is the school located in San Joaquin County, California? school_address')
LIMIT 5
