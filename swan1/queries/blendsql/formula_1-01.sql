WITH temp_cte AS (
SELECT *, 'Location: '||location||', Name: '||name AS key
FROM circuits
)
SELECT {{
    LLMMap(
        'Provide the wiki url.',
        temp_cte.key
    )

}}
FROM temp_cte INNER JOIN races AS T2 ON T2.circuitId = temp_cte.circuitId 
WHERE temp_cte.name = 'Circuit de Barcelona-Catalunya'
