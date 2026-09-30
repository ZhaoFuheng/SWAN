WITH temp_cte AS (
    SELECT *, 'Location: ' || location || ', Name: ' || name AS key
    FROM circuits
)
SELECT ai_complete('Provide the wiki url. key: ' || temp_cte.key || ' Answer with the value only, without any other words.')
FROM temp_cte INNER JOIN races AS T2 ON T2.circuitId = temp_cte.circuitId
WHERE temp_cte.name = 'Circuit de Barcelona-Catalunya'
