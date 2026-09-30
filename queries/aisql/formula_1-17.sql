WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT circuit_data.name
FROM circuit_data
WHERE (ai_filter('Is this Formula 1 circuit in the southern hemisphere? circuit: ' || circuit_data.circuit)
       OR ai_filter('Is this Formula 1 circuit west of 30 degrees west longitude? circuit: ' || circuit_data.circuit))
  AND ai_filter('Is this Formula 1 circuit outside the USA? circuit: ' || circuit_data.circuit)
