SELECT ai_complete('Provide the wiki url. name: ' || constructors.name || ' Answer with the value only, without any other words.') AS person_url
FROM constructorResults AS T1 INNER JOIN constructors ON constructors.constructorId = T1.constructorId
WHERE T1.raceId = 9
ORDER BY T1.points DESC
LIMIT 10
