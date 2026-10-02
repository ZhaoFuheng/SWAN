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
  AND ai_filter('Context:
[circuit]: «' || circuit_data.circuit || '»


Claim: Is this Formula 1 circuit in Spain? circuit')
