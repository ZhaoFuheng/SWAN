WITH driver_data AS (
    SELECT DISTINCT T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key
    FROM drivers AS T1
    INNER JOIN results AS T2 ON T2.driverId = T1.driverId
    WHERE T2.raceId = 592 AND T2.time IS NOT NULL
)
SELECT driver_data.forename, driver_data.surname
FROM driver_data
ORDER BY TRY_CAST(ai_complete('Provide the date of birth. key: ' || driver_data.key
                              || ' Answer with the date only, in YYYY-MM-DD format.') AS DATE) ASC NULLS FIRST
LIMIT 3
