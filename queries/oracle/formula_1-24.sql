WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
)
SELECT race_data.name, race_data.date AS date
FROM race_data
WHERE race_data.year < 2000
  AND race_data.raceId IN (SELECT results.raceId FROM results)
ORDER BY race_data.year DESC, race_data.round DESC
LIMIT 5
