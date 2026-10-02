WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
)
SELECT DISTINCT race_data.name,
    ai_complete('What is the English Wikipedia URL of this Formula 1 race? race: ' || race_data.race
                || ' Answer with the value only, without any other words.') AS url
FROM race_data
WHERE race_data.year = 2017
