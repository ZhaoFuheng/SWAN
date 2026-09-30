WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.School
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode INNER JOIN f ON f.CDSCode = s.CDSCode
WHERE T1.NumTstTakr > 300
  AND (ai_filter('Is this a magnet school, or does it offer a magnet program? school_address: ' || s.school_address)
       OR (ai_filter('Is this a charter school? school_district: ' || f.school_district) AND ai_filter('Is the school located in San Diego County, California? school_address: ' || s.school_address)))
