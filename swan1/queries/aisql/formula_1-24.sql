WITH race_data AS (
    SELECT T1.year || ' ' || T1.name AS key, T1.name, T1.round
    FROM races AS T1
    WHERE T1.year = 1999
)
SELECT race_data.name,
    ai_complete('Provide the race date. key: ' || race_data.key
                || ' Answer with the date only, in YYYY-MM-DD format.') AS date
FROM race_data
ORDER BY race_data.round DESC
LIMIT 5
