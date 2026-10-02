WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT substr(s.CDSCode, 1, 14) AS CDSCode, s.School
FROM s
WHERE (s.Zip LIKE '952%' OR s.Zip LIKE '953%')
  AND s.SOCType = 'Continuation High Schools'
  AND s.StatusType = 'Active' AND s.MailState = 'CA'
  AND s.County = 'San Joaquin'
LIMIT 5
