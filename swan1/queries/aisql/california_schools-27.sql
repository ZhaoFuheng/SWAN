SELECT T1.NumTstTakr
FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
WHERE ai_filter('Is the address located in Fresno City? Street: ' || T2.Street)
