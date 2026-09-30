WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT circuit_data.name
FROM circuit_data
WHERE circuit_data.circuitId IN (SELECT races.circuitId FROM races)
  AND ai_filter('Is this Formula 1 circuit east of the prime meridian? circuit: ' || circuit_data.circuit)
  AND ai_filter('Is this Formula 1 circuit north of 45 degrees latitude? circuit: ' || circuit_data.circuit)
  AND ai_filter('Is this Formula 1 circuit outside Germany? circuit: ' || circuit_data.circuit)
