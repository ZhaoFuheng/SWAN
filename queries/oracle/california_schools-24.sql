SELECT CAST(SUM(CASE WHEN T2.DOC = '54' THEN 1 ELSE 0 END) AS DOUBLE) / SUM(CASE WHEN T2.DOC = '56' THEN 1 ELSE 0 END)
FROM satscores AS D INNER JOIN schools AS T2 ON T2.District = D.dname
WHERE D.rtype = 'D' AND T2.SOCType = 'High Schools (Public)' AND T2.DOC IN ('54', '56')
  AND D.cname = 'Orange'
