WITH race_data AS (
    SELECT T2.raceId, T2.name, T2.year, T2.year || ' ' || T2.name AS key, T1.name AS circuit_name
    FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
)
SELECT DISTINCT race_data.circuit_name
FROM race_data WHERE STRFTIME('%Y-%m', {{
    LLMMap(
        'Provide the race date.',
        'race_data::key'
    )
}}) BETWEEN '1990-06' AND '2000-06' 
GROUP BY race_data.circuit_name
HAVING COUNT(race_data.raceId) = 4
