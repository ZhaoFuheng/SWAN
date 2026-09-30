WITH race_data AS (
    SELECT T2.year || ' ' || T2.name AS key
    FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
    WHERE T1.name = 'Brands Hatch' AND T2.name = 'British Grand Prix' 
    ORDER BY T2.year DESC LIMIT 3
)
SELECT {{
        LLMMap(
            'Provide the race date.',
            'race_data::key'
        )
    }} AS date
FROM race_data
