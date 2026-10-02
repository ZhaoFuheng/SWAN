WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT CAST(COUNT(DISTINCT substr(s.CDSCode, 1, 14)) AS DOUBLE) / 12
FROM s
WHERE s.DOC = '56'
  AND s.County = 'Los Angeles'
  AND substr(s.OpenDate, 1, 4) = '2004'
