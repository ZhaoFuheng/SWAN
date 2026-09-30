WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), summer_races AS (
    SELECT race_data.circuitId AS circuitId, race_data.year AS year
    FROM race_data
    WHERE race_data.year BETWEEN 1990 AND 1999
      AND (race_data.date LIKE '%-06-%' OR race_data.date LIKE '%-07-%' OR race_data.date LIKE '%-08-%')
)
SELECT DISTINCT circuits.name
FROM circuits
INNER JOIN summer_races AS early ON early.circuitId = circuits.circuitId
INNER JOIN summer_races AS late ON late.circuitId = circuits.circuitId
WHERE early.year BETWEEN 1990 AND 1994
  AND late.year BETWEEN 1995 AND 1999
