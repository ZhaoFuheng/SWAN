WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(s.CDSCode)
FROM s INNER JOIN satscores AS T2 ON s.CDSCode = T2.cds
WHERE s.County = 'Sacramento'
  AND T2.NumTstTakr < 100
