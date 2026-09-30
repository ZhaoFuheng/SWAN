WITH driver_data AS (
    SELECT DISTINCT T1.forename || ' ' || T1.surname AS key, fastestLapSpeed
    FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId
    WHERE T2.raceId = 933 AND T2.fastestLapTime IS NOT NULL
)
SELECT {{
    LLMMap(
        'Provide the nationality.',
        'driver_data::key'
    )
}} AS nationality
FROM driver_data
ORDER BY driver_data.fastestLapSpeed DESC
LIMIT 5
