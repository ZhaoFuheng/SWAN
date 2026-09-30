SELECT CAST(COUNT(DISTINCT schools.School) AS DOUBLE) / 12
FROM schools
WHERE schools.DOC = '52'
  AND ai_filter('Is the address located in Alameda County? Street: ' || schools.Street)
  AND strftime(TRY_CAST(schools.OpenDate AS DATE), '%Y') = '1980'
