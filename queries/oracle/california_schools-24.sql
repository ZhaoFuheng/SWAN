WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT CAST(COUNT(DISTINCT CASE WHEN s.DOC = '54' THEN substr(s.CDSCode, 1, 14) END) AS DOUBLE)
       / NULLIF(COUNT(DISTINCT CASE WHEN s.DOC = '56' THEN substr(s.CDSCode, 1, 14) END), 0)
FROM satscores AS D INNER JOIN s ON s.District = D.dname
WHERE substr(s.Zip, 1, 3) IN ('926', '927', '928')
  AND D.rtype = 'D'
  AND D.cname = 'Orange'
  AND s.SOCType = 'High Schools (Public)'
  AND s.DOC IN ('54', '56')
