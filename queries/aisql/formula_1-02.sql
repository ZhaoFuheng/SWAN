WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT races.year, races.name
FROM races
WHERE races.circuitId IN (SELECT circuit_data.circuitId FROM circuit_data
                          WHERE ai_filter('Is this Formula 1 circuit in Germany? circuit: ' || circuit_data.circuit))
LIMIT 5
