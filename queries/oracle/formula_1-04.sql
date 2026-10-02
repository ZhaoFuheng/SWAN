WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT COUNT(DISTINCT drivers.forename || '|' || drivers.surname || '|' || CAST(results.raceId AS VARCHAR))
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN circuit_data ON circuit_data.circuitId = races.circuitId
INNER JOIN drivers ON drivers.driverId = results.driverId
WHERE races.year >= 2010
  AND results.time IS NOT NULL
  AND circuit_data.country = 'Spain'
