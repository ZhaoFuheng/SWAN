WITH driver_data AS (
    SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
    FROM qualifying AS T1
    INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
    WHERE T1.raceId = 355 AND T1.q2 ILIKE '1:40%'
)
SELECT DISTINCT ai_complete('Provide the nationality. key: ' || driver_data.key || ' Answer with the value only, without any other words.') AS nationality
FROM driver_data
