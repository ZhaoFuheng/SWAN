SELECT constructors.name, constructorStandings.points,
    ai_complete('What is the English Wikipedia URL of this Formula 1 constructor? name: ' || constructors.name
                || ' Answer with the value only, without any other words.') AS url
FROM constructorStandings
INNER JOIN races ON races.raceId = constructorStandings.raceId
INNER JOIN constructors ON constructors.constructorId = constructorStandings.constructorId
WHERE races.year = 2009
ORDER BY constructorStandings.points DESC, constructorStandings.constructorStandingsId
LIMIT 5
