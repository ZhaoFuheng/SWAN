WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), november_races AS (
    SELECT race_data.raceId AS raceId
    FROM race_data
    WHERE race_data.date LIKE '%-11-%'
      AND race_data.year = 2015
)
SELECT COUNT(DISTINCT drivers.forename || '|' || drivers.surname || '|' || CAST(results.raceId AS VARCHAR))
FROM november_races
INNER JOIN results ON results.raceId = november_races.raceId
INNER JOIN drivers ON drivers.driverId = results.driverId
WHERE results.time IS NOT NULL
