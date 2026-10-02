WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT circuit_data.name
FROM circuit_data
WHERE ai_filter('Context:
[circuit]: «' || circuit_data.circuit || '»


Claim: Is this Formula 1 circuit in the southern hemisphere? circuit')
LIMIT 3
