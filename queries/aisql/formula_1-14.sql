WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT constructors.name
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN driver_data ON driver_data.driverId = results.driverId
INNER JOIN constructors ON constructors.constructorId = results.constructorId
WHERE races.year >= 2012
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Is this Formula 1 driver Brazilian? driver')
