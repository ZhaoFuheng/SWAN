SELECT CASE WHEN results.time IS NOT NULL
            THEN ai_complete('What is the nationality of this Formula 1 constructor? name: ' || constructors.name
                             || ' Answer with the value only, without any other words.')
            END AS constructor_nationality,
    COUNT(DISTINCT drivers.forename || '|' || drivers.surname || '|' || CAST(results.raceId AS VARCHAR)) AS results
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN constructors ON constructors.constructorId = results.constructorId
INNER JOIN drivers ON drivers.driverId = results.driverId
WHERE races.year = 2008
GROUP BY constructor_nationality
