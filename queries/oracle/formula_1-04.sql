WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT COUNT(*)
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN circuit_data ON circuit_data.circuitId = races.circuitId
WHERE races.year >= 2010
  AND results.time IS NOT NULL
  AND circuit_data.country = 'Spain'
