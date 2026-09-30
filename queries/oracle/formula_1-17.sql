WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT circuit_data.name
FROM circuit_data
WHERE (circuit_data.lat < 0
       OR circuit_data.lng < -30)
  AND circuit_data.country <> 'USA'
