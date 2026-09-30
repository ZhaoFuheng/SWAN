SELECT COUNT(T2.raceId)
FROM circuits AS T1
INNER JOIN races AS T2 ON T2.circuitId = T1.circuitId
WHERE ai_filter('Is the location outside Asia and Europe? location: ' || T1.location)
  AND T2.year = 2010
