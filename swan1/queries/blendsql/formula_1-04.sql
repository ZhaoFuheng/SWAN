SELECT DISTINCT T2.name 
FROM circuits AS T1 
INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId 
WHERE {{
    LLMMap(
        'Provide the country name.',
        T1.location
    )
}} = 'Spain'
