WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT race_data.year, race_data.name
FROM race_data
INNER JOIN circuit_data ON circuit_data.circuitId = race_data.circuitId
WHERE race_data.year >= 2000
  AND circuit_data.lat > 0
  AND circuit_data.country <> 'USA'
  AND circuit_data.lng < 0
  AND race_data.date LIKE '%-06-%'
