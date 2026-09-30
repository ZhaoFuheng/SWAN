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
  AND ai_filter('Was this Formula 1 race held in July? race: ' || race_data.race)
  AND ai_filter('Is this Formula 1 circuit north of 51.5 degrees latitude? circuit: ' || circuit_data.circuit)
  AND ai_filter('Is this Formula 1 circuit in the UK? circuit: ' || circuit_data.circuit)
