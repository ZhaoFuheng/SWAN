WITH temp AS (
    SELECT *, 
        'District: ' || `District Name` || ' and School: ' || `School Name` AS district_school_key
    FROM frpm
), 
temp2 AS ( 
    SELECT *, {{
        LLMMap(
            'What is the school Charter Funding Type?', 
            'temp::district_school_key'
        )
    }} AS FundingType
    FROM temp
)
SELECT T1.sname, temp2.FundingType
FROM satscores AS T1 INNER JOIN temp2 ON T1.cds = temp2.CDSCode 
WHERE temp2.`District Name` LIKE 'Riverside%' 
GROUP BY T1.sname, temp2.FundingType
HAVING CAST(SUM(T1.AvgScrMath) AS REAL) / COUNT(T1.cds) > 400
