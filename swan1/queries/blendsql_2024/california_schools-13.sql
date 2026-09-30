WITH temp AS (
    SELECT *, 
        'District: ' || `District Name` || ' and School: ' || `School Name` AS district_school_key 
    FROM frpm
)
SELECT COUNT(*)
FROM temp AS T1
WHERE {{
        LLMMap(
            'Is the school locally funded under the charter funding type?',
            'T1::district_school_key '
        )
        }} = TRUE
AND (T1.`Enrollment (K-12)` - T1.`Enrollment (Ages 5-17)`) > 
            (SELECT AVG(T3.`Enrollment (K-12)` - T3.`Enrollment (Ages 5-17)`) 
            FROM temp as T3 WHERE {{
        LLMMap(
            'Is the school locally funded under the charter funding type?',
            'T3::district_school_key '
        )
        }} = TRUE
    )
