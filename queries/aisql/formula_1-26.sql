WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname,
    ai_complete('What is the nationality of this Formula 1 driver? driver: ' || driver_data.driver
                || ' Answer with the value only, without any other words.') AS nationality
FROM driverStandings
INNER JOIN races ON races.raceId = driverStandings.raceId
INNER JOIN driver_data ON driver_data.driverId = driverStandings.driverId
WHERE races.year >= 2000 AND driverStandings.position = 1
