WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT races.name, driver_data.forename, driver_data.surname, driver_data.nationality AS nationality
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN driver_data ON driver_data.driverId = results.driverId
WHERE races.year = 2015 AND results.fastestLapSpeed IS NOT NULL
ORDER BY CAST(results.fastestLapSpeed AS DOUBLE) DESC, results.resultId
LIMIT 5
