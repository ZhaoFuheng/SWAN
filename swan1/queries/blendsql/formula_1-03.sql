SELECT COUNT(T2.raceId) 
FROM circuits AS T1 
INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId 
WHERE {{
    LLMMap(
        'Is the location outside Asia and Europe?',
        T1.location
    )
}} = TRUE
AND T2.year = 2010
