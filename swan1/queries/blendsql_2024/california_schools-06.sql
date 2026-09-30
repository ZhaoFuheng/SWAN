WITH temp AS (
SELECT T1.Phone, 'Street: ' || T1.Street || ' and School: ' || T1.School AS address
    FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds 
    ORDER BY CAST(T2.NumGE1500 AS REAL) / T2.NumTstTakr DESC LIMIT 10
)
SELECT temp.Phone, {{
    LLMMap(
        'Provide the city name based on the address.',
        'temp::address'
    )
}} AS City FROM temp
