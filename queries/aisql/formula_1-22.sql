WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname, CAST(results.fastestLapSpeed AS DOUBLE) AS speed
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN driver_data ON driver_data.driverId = results.driverId
WHERE races.year >= 2014
  AND results.fastestLapSpeed IS NOT NULL
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Is this Formula 1 driver German? driver')
ORDER BY speed DESC, driver_data.forename, driver_data.surname
LIMIT 1
