WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT races.year,
    ai_complete('Which country is this Formula 1 circuit in? circuit: ' || circuit_data.circuit
                || ' Answer with the value only, without any other words.') AS country
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE circuit_data.location = 'Shanghai'
