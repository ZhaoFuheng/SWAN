WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
)
SELECT race_data.name,
    ai_complete('On what date was this Formula 1 race held? race: ' || race_data.race || ' Answer with the date only, in YYYY-MM-DD format.') AS date
FROM race_data
WHERE race_data.year < 2000
  AND race_data.raceId IN (SELECT results.raceId FROM results)
ORDER BY race_data.year DESC, race_data.round DESC, race_data.raceId
LIMIT 5
