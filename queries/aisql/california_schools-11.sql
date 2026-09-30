WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT T1.sname,
    ai_classify('What is the charter funding type of the school? school_district: ' || f.school_district,
                ['Directly funded', 'Locally funded']) AS FundingType
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode INNER JOIN f ON f.CDSCode = s.CDSCode
WHERE T1.AvgScrMath > 400
  AND ai_filter('Is this a charter school? school_district: ' || f.school_district)
  AND ai_classify('Is this a magnet school, or does it offer a magnet program? school_address: ' || s.school_address, ['Yes', 'No']) = 'No'
  AND ai_filter('Is the school located in Riverside County, California? school_address: ' || s.school_address)
