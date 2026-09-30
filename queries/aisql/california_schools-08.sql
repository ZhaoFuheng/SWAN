WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT COUNT(s.CDSCode)
FROM s INNER JOIN satscores AS T2 ON s.CDSCode = T2.cds INNER JOIN f ON s.CDSCode = f.CDSCode
WHERE T2.NumTstTakr BETWEEN 100 AND 250
  AND ai_classify('Is this a magnet school, or does it offer a magnet program? school_address: ' || s.school_address, ['Yes', 'No']) = 'No'
  AND ai_filter('Is this a charter school? school_district: ' || f.school_district)
  AND ai_filter('Is this school a directly funded charter school? school_district: ' || f.school_district)
  AND ai_filter('Is the school located in Los Angeles County, California? school_address: ' || s.school_address)
