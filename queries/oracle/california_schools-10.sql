WITH districts AS (
    SELECT dname, cname FROM satscores WHERE rtype = 'D'
)
SELECT T2.School
FROM districts AS D INNER JOIN schools AS T2 ON T2.District = D.dname INNER JOIN satscores AS T1 ON T1.cds = T2.CDSCode
WHERE T1.NumTstTakr >= 100
  AND D.cname = 'Orange'
ORDER BY T1.NumTstTakr DESC, T2.School, T2.CDSCode
LIMIT 1
