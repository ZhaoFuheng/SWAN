WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
)
SELECT race_data.name, race_data.url AS url
FROM race_data
WHERE race_data.year = 2017
