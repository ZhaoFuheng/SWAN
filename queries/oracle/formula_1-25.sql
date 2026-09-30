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
WHERE race_data.year BETWEEN 1980 AND 1999
  AND race_data.date LIKE '%-07-%'
  AND circuit_data.lat > 51.5
  AND circuit_data.country = 'UK'
