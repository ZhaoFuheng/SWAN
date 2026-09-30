WITH f AS (
    SELECT *, 'School: ' || "School Name" || '; District: ' || "District Name" AS school_district
    FROM frpm
),
s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT f."School Name", s.Street, ai_complete('In which city is the school located? school_address: ' || s.school_address || ' Answer with the value only, without any other words.') AS City, s.Zip, s.State
FROM f INNER JOIN s ON f.CDSCode = s.CDSCode
WHERE f."School Type" = 'High Schools (Public)' AND f."FRPM Count (Ages 5-17)" > 800
  AND ai_classify('What is the educational option type of the school? school_district: ' || f.school_district,
                  ['Alternative School of Choice', 'Community Day School', 'Continuation School', 'County Community School', 'District Special Education Consortia School', 'Home and Hospital', 'Juvenile Court School', 'Opportunity School', 'Special Education School', 'State Special School', 'Traditional']) = 'Traditional'
  AND ai_classify('Is this a charter school? school_district: ' || f.school_district, ['Yes', 'No']) = 'No'
  AND ai_filter('Is the school located in Monterey County, California? school_address: ' || s.school_address)
