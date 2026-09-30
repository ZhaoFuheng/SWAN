WITH location_data AS (
    SELECT *,
        TRY_CAST(ai_complete('Provide the latitude based on location (float). location: ' || circuits.location
                             || ' Answer with the number only.') AS DOUBLE) AS lat,
        TRY_CAST(ai_complete('Provide the longitude based on location (float). location: ' || circuits.location
                             || ' Answer with the number only.') AS DOUBLE) AS lng
    FROM circuits
)
SELECT DISTINCT location_data.lat, location_data.lng
FROM location_data INNER JOIN races AS T2 ON T2.circuitId = location_data.circuitId
WHERE T2.name = 'Australian Grand Prix'
