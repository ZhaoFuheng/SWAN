WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname, driver_data.url AS url
FROM lapTimes
INNER JOIN driver_data ON driver_data.driverId = lapTimes.driverId
WHERE lapTimes.raceId = 161 AND lapTimes.time LIKE '1:27%'
