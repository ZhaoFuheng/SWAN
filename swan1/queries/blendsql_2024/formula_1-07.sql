WITH location_data AS (
SELECT *, {{
    LLMMap(
        'Provide the latitude based on location (float).',
        'circuits::location'
        )
    }} AS lat, {{
    LLMMap(
        'Provide the longitude based on location (float).',
        'circuits::location'
    )
}} AS lng
FROM circuits
)
SELECT DISTINCT location_data.lat, location_data.lng
FROM location_data INNER JOIN races AS T2 ON T2.circuitId = location_data.circuitId
WHERE T2.name = 'Abu Dhabi Grand Prix'
