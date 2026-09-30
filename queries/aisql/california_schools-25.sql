SELECT ai_complete('In which California county is this school district? Give the county name without the word County. dname: ' || D.dname || ' Answer with the value only, without any other words.') AS county, COUNT(*) AS n
FROM satscores AS D INNER JOIN schools AS T2 ON T2.District = D.dname
WHERE D.rtype = 'D' AND T2.StatusType = 'Closed'
GROUP BY county
ORDER BY n DESC, county
LIMIT 1
