SELECT ai_complete('Provide the school website address for each school. School: ' || schools.School || ' Answer with the value only, without any other words.') AS Website
FROM satscores INNER JOIN schools ON satscores.cds = schools.CDSCode
WHERE ai_filter('Is the address located in Los Angeles County? Street: ' || schools.Street)
  AND satscores.NumTstTakr >= 150 AND satscores.NumTstTakr <= 160
