SELECT COUNT(frpm.CDSCode)
FROM frpm JOIN schools ON frpm.CDSCode = schools.CDSCode
WHERE frpm."Free Meal Count (K-12)" > 500 AND frpm."Free Meal Count (K-12)" < 700
  AND ai_filter('Is the address located in Los Angeles County? Street: ' || schools.Street)
