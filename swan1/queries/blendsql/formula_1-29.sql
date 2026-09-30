WITH circuit_data AS (
    SELECT T1.circuitId, T1.name AS circuit_name, T1.location, T1.location || ' ' || T1.name AS key
    FROM circuits AS T1
)
SELECT  circuit_data.circuit_name,  circuit_data.location, T2.name AS race_name
FROM circuit_data INNER JOIN races AS T2 ON T2.circuitId = circuit_data.circuitId
WHERE {{
    LLMMap(
        'Was it in USA?',
        circuit_data.key
    )
}} = TRUE
AND T2.year = 2006
