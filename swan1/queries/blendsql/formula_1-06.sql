SELECT DISTINCT {{
    LLMMap(
        'Provide the wiki url.',
        circuits.name
    )
}} AS url
FROM circuits INNER JOIN races AS T2 ON T2.circuitId = circuits.circuitId
WHERE circuits.name = 'Sepang International Circuit'
