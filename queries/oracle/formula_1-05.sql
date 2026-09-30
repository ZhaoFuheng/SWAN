WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT circuit_data.name
FROM circuit_data
WHERE circuit_data.lat < 0
LIMIT 3
