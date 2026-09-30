WITH fastest AS (
    SELECT T1.forename || ' ' || T1.surname AS key
    FROM drivers AS T1
    INNER JOIN results AS T2 ON T2.driverId = T1.driverId
    WHERE T2.fastestLapTime IS NOT NULL
    ORDER BY T2.fastestLapSpeed DESC
    LIMIT 1
)
SELECT ai_complete('Provide the nationality. key: ' || fastest.key || ' Answer with the value only, without any other words.') AS nationality
FROM fastest
