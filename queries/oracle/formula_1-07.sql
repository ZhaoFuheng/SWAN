WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT circuit_data.name
FROM circuit_data
WHERE circuit_data.circuitId IN (SELECT races.circuitId FROM races)
  AND circuit_data.lng > 0
  AND circuit_data.lat > 45
  AND circuit_data.country <> 'Germany'
