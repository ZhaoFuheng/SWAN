WITH temp AS (
SELECT *, 'Location: '||location||', Name: '||name AS key
FROM circuits
)
SELECT {{
    LLMMap(
        'Provide the wiki url.',
        'temp::key'
    )

}}
FROM temp INNER JOIN races AS T2 ON T2.circuitId = temp.circuitId 
WHERE temp.name = 'Circuit de Barcelona-Catalunya'
