WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(s.CDSCode)
FROM s INNER JOIN satscores AS T2 ON s.CDSCode = T2.cds
WHERE ai_filter('Is the school located in Sacramento County, California? school_address: ' || s.school_address)
  AND T2.NumTstTakr < 100
