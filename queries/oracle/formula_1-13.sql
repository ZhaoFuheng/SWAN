WITH fastest AS (
    SELECT DISTINCT races.name AS race_name, drivers.forename, drivers.surname,
        drivers.forename || ' ' || drivers.surname AS driver, drivers.nationality,
        CAST(results.fastestLapSpeed AS DOUBLE) AS speed
    FROM results
    INNER JOIN races ON races.raceId = results.raceId
    INNER JOIN drivers ON drivers.driverId = results.driverId
    WHERE races.year = 2015 AND results.fastestLapSpeed IS NOT NULL
)
SELECT fastest.race_name, fastest.forename, fastest.surname, fastest.nationality AS nationality
FROM fastest
ORDER BY fastest.speed DESC, fastest.race_name, fastest.forename, fastest.surname
LIMIT 5
