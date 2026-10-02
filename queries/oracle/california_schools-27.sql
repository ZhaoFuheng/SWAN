WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
),
fresno_schools AS (
    SELECT DISTINCT substr(s.CDSCode, 1, 14) AS cds, T1.NumTstTakr
    FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
    WHERE T1.NumTstTakr >= 100
      AND s.City = 'Fresno'
)
SELECT SUM(fresno_schools.NumTstTakr)
FROM fresno_schools
