WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT COUNT(DISTINCT races.name || '|' || CAST(races.year AS VARCHAR))
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE ai_filter('Context:
[circuit]: «' || circuit_data.circuit || '»


Claim: Is this Formula 1 circuit in North or South America? circuit')
  AND races.year = 2010
