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
  AND ai_filter('Is this Formula 1 circuit north of the equator? circuit: ' || circuit_data.circuit)
  AND ai_filter('Is this Formula 1 circuit outside the USA? circuit: ' || circuit_data.circuit)
  AND ai_filter('Is this Formula 1 circuit west of the prime meridian? circuit: ' || circuit_data.circuit)
  AND ai_filter('Was this Formula 1 race held in June? race: ' || race_data.race)
