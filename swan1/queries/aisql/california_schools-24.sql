SELECT CAST(SUM(CASE WHEN schools.DOC = '54' THEN 1 ELSE 0 END) AS DOUBLE)
       / NULLIF(SUM(CASE WHEN schools.DOC = '52' THEN 1 ELSE 0 END), 0)
FROM schools
WHERE schools.StatusType = 'Merged'
  AND ai_filter('Is the address located in Orange County? Street: ' || schools.Street)
