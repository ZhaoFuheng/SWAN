WITH driver_data AS (
    SELECT DISTINCT  T1.forename || ' ' || T1.surname AS key, T1.forename, T1.surname
    FROM drivers AS T1 INNER JOIN results AS T2 ON T2.driverId = T1.driverId
    WHERE T2.raceId = 872 AND T2.time IS NOT NULL
)

SELECT 
    driver_data.forename, 
    driver_data.surname
FROM driver_data
ORDER BY {{
    LLMMap(
        'Provide the date of birth.',
        driver_data.key
    )
}} DESC LIMIT 5
