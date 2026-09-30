WITH temp_cte AS (
    SELECT *, 
        'District: ' || `District Name` || ' and School: ' || `School Name` AS district_school_key 
    FROM frpm
) SELECT COUNT(T2.`School Code`) 
    FROM satscores AS T1 INNER JOIN temp_cte AS T2 ON T1.cds = T2.CDSCode
    WHERE T1.AvgScrMath > 560 AND {{
        LLMMap(
            'Is the school funded directly under the charter funding type?',
            T2.district_school_key
        )
        }} = TRUE
