WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), may_races AS (
    SELECT race_data.raceId AS raceId
    FROM race_data
    WHERE race_data.date LIKE '%-05-%'
      AND race_data.year = 1983
)
SELECT CAST(COUNT(CASE WHEN results.time IS NOT NULL THEN results.driverId END) AS DOUBLE) * 100
       / COUNT(results.driverId)
FROM may_races
INNER JOIN results ON results.raceId = may_races.raceId
