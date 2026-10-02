WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), may_races AS (
    SELECT race_data.raceId AS raceId
    FROM race_data
    WHERE race_data.date LIKE '%-05-%'
      AND race_data.year = 1983
)
SELECT CAST(COUNT(DISTINCT CASE WHEN results.time IS NOT NULL
                           THEN drivers.forename || '|' || drivers.surname || '|' || CAST(results.raceId AS VARCHAR) END) AS DOUBLE) * 100
       / COUNT(DISTINCT drivers.forename || '|' || drivers.surname || '|' || CAST(results.raceId AS VARCHAR))
FROM may_races
INNER JOIN results ON results.raceId = may_races.raceId
INNER JOIN drivers ON drivers.driverId = results.driverId
