WITH driver_data AS (
    SELECT DISTINCT T2.forename || ' ' || T2.surname AS key
    FROM qualifying AS T1
    INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
    WHERE T1.raceId = 45 AND T1.q3 LIKE '1:33%'
)
SELECT {{
    LLMMap(
        'Provide the F1 driver abbreviated code.',
        driver_data.key
    )
}} AS driver_code
FROM driver_data
