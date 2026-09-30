WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT races.year, circuit_data.country AS country
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE circuit_data.location = 'Shanghai'
