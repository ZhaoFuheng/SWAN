SELECT T2.year, {{
    LLMMap(
        'Provide the country name',
        'circuits::location'
    )

}}
FROM circuits INNER JOIN races AS T2 ON T2.circuitId = circuits.circuitId 
WHERE circuits.location = 'Shanghai'
