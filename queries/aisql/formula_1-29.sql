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
  AND ai_filter('Context:
[circuit]: «' || circuit_data.circuit || '»


Claim: Is this Formula 1 circuit north of the equator? circuit')
  AND ai_filter('Context:
[circuit]: «' || circuit_data.circuit || '»


Claim: Is this Formula 1 circuit outside the USA? circuit')
  AND ai_filter('Context:
[circuit]: «' || circuit_data.circuit || '»


Claim: Is this Formula 1 circuit west of the prime meridian? circuit')
  AND ai_filter('Context:
[race]: «' || race_data.race || '»


Claim: Was this Formula 1 race held in June? race')
