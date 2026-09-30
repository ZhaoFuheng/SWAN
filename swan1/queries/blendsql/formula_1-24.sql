WITH race_data AS (
    SELECT T1.year || ' ' || T1.name AS key, T1.name, T1.round
    FROM races AS T1
    WHERE T1.year = 1999
)
SELECT 
    race_data.name, 
    {{
        LLMMap(
            'Provide the race date.',
            race_data.key
        )
    }} AS date
FROM race_data
ORDER BY race_data.round DESC
LIMIT 5
