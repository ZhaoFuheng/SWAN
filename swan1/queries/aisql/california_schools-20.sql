SELECT T2.School
FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
WHERE ai_filter('Is the school operate exclusively virtual? School: ' || T2.School)
ORDER BY T1.AvgScrRead DESC
LIMIT 5
