SELECT DISTINCT ai_complete('Provide the wiki url. name: ' || circuits.name || ' Answer with the value only, without any other words.') AS url
FROM circuits INNER JOIN races AS T2 ON T2.circuitId = circuits.circuitId
WHERE circuits.name = 'Sepang International Circuit'
