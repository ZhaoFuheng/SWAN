SELECT constructors.name, constructorStandings.points, constructors.url AS url
FROM constructorStandings
INNER JOIN races ON races.raceId = constructorStandings.raceId
INNER JOIN constructors ON constructors.constructorId = constructorStandings.constructorId
WHERE races.year = 2009
ORDER BY constructorStandings.points DESC, constructors.name, races.name
LIMIT 5
