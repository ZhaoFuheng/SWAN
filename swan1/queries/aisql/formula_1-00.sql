SELECT T2.year, ai_complete('Provide the country name location: ' || circuits.location || ' Answer with the value only, without any other words.')
FROM circuits INNER JOIN races AS T2 ON T2.circuitId = circuits.circuitId
WHERE circuits.location = 'Shanghai'
