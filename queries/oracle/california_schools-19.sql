WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
),
fresno_schools AS (
    SELECT DISTINCT substr(s.CDSCode, 1, 14) AS cds, T1.NumTstTakr
    FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
    WHERE s.OpenDate BETWEEN '1990-01-01' AND '1999-12-31'
      AND s.County = 'Fresno'
)
SELECT AVG(fresno_schools.NumTstTakr)
FROM fresno_schools
