SELECT CASE WHEN results.time IS NOT NULL
            THEN constructors.nationality
            END AS constructor_nationality,
    COUNT(*) AS results
FROM results
INNER JOIN races ON races.raceId = results.raceId
INNER JOIN constructors ON constructors.constructorId = results.constructorId
WHERE races.year = 2008
GROUP BY constructor_nationality
