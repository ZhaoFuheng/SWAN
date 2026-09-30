SELECT schools.Street, {{
    LLMMap (
        'Provide the city name based on the address.',
        schools.Street
        )
}} AS City, schools.Zip, schools.State 
    FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode 
    ORDER BY CAST(T1.NumGE1500 AS REAL) / T1.NumTstTakr ASC LIMIT 10
