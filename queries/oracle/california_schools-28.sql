WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.CDSCode, s.School
FROM s
WHERE s.SOCType = 'Continuation High Schools' AND s.StatusType = 'Active' AND s.MailState = 'CA'
  AND s.County = 'San Joaquin'
LIMIT 5
