SELECT T2.School
FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
WHERE T1.NumTstTakr > 500
  AND ai_filter('Is the school at the address a magnet school? Street: ' || T2.Street)
