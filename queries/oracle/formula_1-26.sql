WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname, driver_data.nationality AS nationality
FROM driverStandings
INNER JOIN races ON races.raceId = driverStandings.raceId
INNER JOIN driver_data ON driver_data.driverId = driverStandings.driverId
WHERE races.year >= 2000 AND driverStandings.position = 1
