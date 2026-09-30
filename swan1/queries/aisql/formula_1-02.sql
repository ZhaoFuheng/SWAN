SELECT DISTINCT T2.name
FROM circuits AS T1 INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
WHERE trim(ai_complete('Provide the country name. location: ' || T1.location || ' Answer with the value only, without any other words.')) = 'Germany'
