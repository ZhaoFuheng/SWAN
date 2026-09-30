WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT AVG(T1.NumTstTakr)
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE s.OpenDate BETWEEN '1990-01-01' AND '1999-12-31'
  AND ai_filter('Is the school located in Fresno County, California? school_address: ' || s.school_address)
