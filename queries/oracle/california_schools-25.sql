SELECT D.cname AS county, COUNT(*) AS n
FROM satscores AS D INNER JOIN schools AS T2 ON T2.District = D.dname
WHERE D.rtype = 'D' AND T2.StatusType = 'Closed'
GROUP BY county
ORDER BY n DESC, county
LIMIT 1
