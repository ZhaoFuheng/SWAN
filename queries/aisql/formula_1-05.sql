WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT circuit_data.name
FROM circuit_data
WHERE ai_filter('Is this Formula 1 circuit in the southern hemisphere? circuit: ' || circuit_data.circuit)
LIMIT 3
