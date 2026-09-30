WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
)
SELECT "Free Meal Count (Ages 5-17)" / "Enrollment (Ages 5-17)"
FROM temp_cte
WHERE "Free Meal Count (Ages 5-17)" / "Enrollment (Ages 5-17)" IS NOT NULL
  AND ai_classify(
        'What is the educational option type of the school? district_school_key: ' || district_school_key,
        ['Traditional', 'Juvenile Court School', 'County Community School', 'State Special School',
         'Alternative School of Choice', 'Continuation School', 'Special Education School',
         'Community Day School', 'Home and Hospital', 'Opportunity School', 'Youth Authority School',
         'District Special Education Consortia School']
      ) = 'Continuation School'
ORDER BY "Free Meal Count (Ages 5-17)" / "Enrollment (Ages 5-17)" ASC
LIMIT 10
