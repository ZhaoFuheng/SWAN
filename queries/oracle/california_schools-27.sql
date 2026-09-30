WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT SUM(T1.NumTstTakr)
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.NumTstTakr >= 100
  AND s.City = 'Fresno'
