WITH circuit_data AS (
    SELECT *, circuits.name || ', ' || circuits.location AS circuit
    FROM circuits
)
SELECT DISTINCT races.year,
    ai_complete('What is the English Wikipedia URL of this Formula 1 circuit? circuit: ' || circuit_data.circuit
                || ' Answer with the value only, without any other words.') AS url
FROM circuit_data
INNER JOIN races ON races.circuitId = circuit_data.circuitId
WHERE circuit_data.name = 'Sepang International Circuit'
