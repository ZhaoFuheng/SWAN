WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT CAST(COUNT(*) AS DOUBLE) / 12
FROM s
WHERE s.DOC = '56'
  AND ai_filter('Is the school located in Los Angeles County, California? school_address: ' || s.school_address)
  AND substr(s.OpenDate, 1, 4) = '2004'
