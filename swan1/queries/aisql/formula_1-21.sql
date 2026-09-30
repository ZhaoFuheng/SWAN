WITH race_data AS (
    SELECT DISTINCT T2.driverId, T1.year || ' ' || T1.name AS key
    FROM races AS T1 INNER JOIN results AS T2 ON T2.raceId = T1.raceId
        AND T2.time IS NOT NULL
)
SELECT COUNT(driverId)
FROM race_data
WHERE ai_filter('Was the race on 2015-11-29? key: ' || race_data.key)
