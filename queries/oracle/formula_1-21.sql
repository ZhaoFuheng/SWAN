WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), november_races AS (
    SELECT race_data.raceId AS raceId
    FROM race_data
    WHERE race_data.date LIKE '%-11-%'
      AND race_data.year = 2015
)
SELECT COUNT(results.driverId)
FROM november_races
INNER JOIN results ON results.raceId = november_races.raceId
WHERE results.time IS NOT NULL
