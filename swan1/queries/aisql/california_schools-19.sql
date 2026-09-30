SELECT AVG(T1.NumTstTakr)
FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
WHERE strftime(TRY_CAST(schools.OpenDate AS DATE), '%Y') = '1980'
  AND ai_filter('Is the address located in Fresno County? Street: ' || schools.Street)
