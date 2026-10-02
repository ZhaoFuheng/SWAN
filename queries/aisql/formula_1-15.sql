WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname
FROM results
INNER JOIN driver_data ON driver_data.driverId = results.driverId
WHERE results.raceId = 872 AND results.time IS NOT NULL
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Is this Formula 1 driver European? driver')
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Was this Formula 1 driver born in 1985 or later? driver')
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Is this Formula 1 driver not German? driver')
