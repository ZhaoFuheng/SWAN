WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
)
SELECT COUNT(*)
FROM temp_cte AS T1
WHERE ai_filter('Is the school locally funded under the charter funding type? district_school_key: ' || T1.district_school_key)
  AND (T1."Enrollment (K-12)" - T1."Enrollment (Ages 5-17)") >
      (SELECT AVG(T3."Enrollment (K-12)" - T3."Enrollment (Ages 5-17)")
       FROM temp_cte AS T3
       WHERE ai_filter('Is the school locally funded under the charter funding type? district_school_key: ' || T3.district_school_key))
