WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT T1."District Name"
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE s.Zip LIKE '945%'
  AND s.City = 'Hayward'
