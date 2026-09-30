WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT races.year, circuit_data.url AS url
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE circuit_data.name = 'Sepang International Circuit'
