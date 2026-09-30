SELECT ai_agg(list(key), 'Where is he from?' || ' Answer with the value only, without any other words.')
FROM (
    SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
    FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
    WHERE T1.raceId = 347 AND T1.q2 ILIKE '1:15%'
)
