WITH temp_cte AS (
SELECT T1.`School Name` , 'Street: ' || T2.Street || ' and School: ' || T2.School AS address
    FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
    WHERE T1.`Free Meal Count (Ages 5-17)` BETWEEN 1910 AND 2000 
)
SELECT {{
    LLMMap(
        'Provide the website based on the school address.',
        temp_cte.address
    )
}} AS Website, `School Name`
FROM temp_cte
