WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname,
    ai_complete('What is the English Wikipedia URL of this Formula 1 driver? driver: ' || driver_data.driver
                || ' Answer with the value only, without any other words.') AS url
FROM lapTimes
INNER JOIN driver_data ON driver_data.driverId = lapTimes.driverId
WHERE lapTimes.raceId = 161 AND lapTimes.time LIKE '1:27%'
