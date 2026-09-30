WITH temp AS (
    SELECT *, 
        'District: ' || `District Name` || ' and School: ' || `School Name` AS district_school_key 
    FROM frpm
)
SELECT T2.Phone 
  FROM temp AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode 
    WHERE T2.OpenDate > '2000-01-01'
    AND {{
        LLMMap(
            'Is this a charter school?',
            'temp::district_school_key '
        )
        }} = TRUE
    AND {{
        LLMMap(
            'Is the school funded directly under the charter funding type?',
            'temp::district_school_key '
        )
        }} = TRUE
