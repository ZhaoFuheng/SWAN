WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname, results.position,
    CASE WHEN results.time IS NOT NULL
         THEN ai_complete('What is the date of birth of this Formula 1 driver? driver: ' || driver_data.driver
                          || ' Answer with the date only, in YYYY-MM-DD format.')
    END AS dob
FROM driver_data
INNER JOIN results ON results.driverId = driver_data.driverId
WHERE results.raceId = 872 AND results.position <= 10
