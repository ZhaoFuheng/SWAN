WITH driver_data AS (
    SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
    FROM qualifying AS T1
    INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
    WHERE T1.raceId = 45 AND T1.q3 ILIKE '1:33%'
)
SELECT ai_complete('Provide the F1 driver abbreviated code. key: ' || driver_data.key || ' Answer with the value only, without any other words.') AS driver_code
FROM driver_data
