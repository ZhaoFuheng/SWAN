WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT s.School, s.Phone
FROM f INNER JOIN s ON f.CDSCode = s.CDSCode
WHERE s.OpenDate > '2012-01-01'
  AND ai_filter('Context:
[school_district]: «' || f.school_district || '»


Claim: Is this a charter school? school_district')
  AND ai_filter('Context:
[school_district]: «' || f.school_district || '»


Claim: Is this school a directly funded charter school? school_district')
  AND ai_filter('Context:
[school_address]: «' || s.school_address || '»


Claim: Is the school located in Fresno County, California? school_address')
