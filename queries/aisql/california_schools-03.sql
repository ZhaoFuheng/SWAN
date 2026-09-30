WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.School, s.Phone
FROM f INNER JOIN s ON f.CDSCode = s.CDSCode
WHERE s.OpenDate > '2012-01-01'
  AND ai_filter('Is this a charter school? school_district: ' || f.school_district)
  AND ai_filter('Is this school a directly funded charter school? school_district: ' || f.school_district)
  AND ai_filter('Is the school located in Fresno County, California? school_address: ' || s.school_address)
