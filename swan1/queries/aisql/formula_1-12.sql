WITH driver_data AS (
    SELECT DISTINCT T2.driverId, T2.forename, T2.surname, T2.forename || ' ' || T2.surname AS key
    FROM lapTimes AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
    WHERE T1.raceId = 161 AND T1.time ILIKE '1:27%'
)
SELECT DISTINCT driver_data.forename, driver_data.surname,
    ai_complete('Provide the wiki url. key: ' || driver_data.key || ' Answer with the value only, without any other words.') AS person_url
FROM driver_data
