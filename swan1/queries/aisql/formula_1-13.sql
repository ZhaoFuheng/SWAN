WITH driver_data AS (
    SELECT DISTINCT T1.forename || ' ' || T1.surname AS key, fastestLapSpeed
    FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId
    WHERE T2.raceId = 933 AND T2.fastestLapTime IS NOT NULL
)
SELECT ai_complete('Provide the nationality. key: ' || driver_data.key || ' Answer with the value only, without any other words.') AS nationality
FROM driver_data
ORDER BY driver_data.fastestLapSpeed DESC
LIMIT 5
