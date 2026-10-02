WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT races.year, races.name
FROM races
WHERE races.circuitId IN (SELECT circuit_data.circuitId FROM circuit_data
                          WHERE circuit_data.country = 'Germany')
LIMIT 5
