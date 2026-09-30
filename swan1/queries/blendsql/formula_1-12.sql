WITH driver_data AS (
    SELECT DISTINCT T2.driverId, T2.forename, T2.surname, T2.forename || ' ' || T2.surname AS key
    FROM lapTimes AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId
    WHERE T1.raceId = 161 AND T1.time LIKE '1:27%'
)
SELECT DISTINCT driver_data.forename, driver_data.surname, {{
        LLMMap(
            'Provide the wiki url.',
            driver_data.key
        )
    }} AS person_url
FROM driver_data
