WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT COUNT(races.raceId)
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE ai_filter('Is this Formula 1 circuit in North or South America? circuit: ' || circuit_data.circuit)
  AND races.year = 2010
