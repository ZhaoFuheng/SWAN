WITH temp AS (
    SELECT *, 
        'District: ' || `District Name` || ' and School: ' || `School Name` AS district_school_key 
    FROM frpm
)
SELECT T2.AdmEmail1 
    FROM temp AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode 
    WHERE {{
        LLMMap(
            'Is this a charter school?',
            'temp::district_school_key '
        )
        }} = TRUE
    ORDER BY T1.`Enrollment (K-12)` ASC LIMIT 1
