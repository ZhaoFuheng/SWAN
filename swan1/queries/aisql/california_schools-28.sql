SELECT COUNT(schools.CDSCode)
FROM schools
WHERE schools.MailState = 'CA' AND schools.StatusType = 'Active'
  AND ai_filter('Is the address located in San Joaquin City? Street: ' || schools.Street)
