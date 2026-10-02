WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT COUNT(DISTINCT races.name || '|' || CAST(races.year AS VARCHAR))
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE circuit_data.country IN ('USA', 'Canada', 'Mexico', 'Brazil', 'Argentina')
  AND races.year = 2010
