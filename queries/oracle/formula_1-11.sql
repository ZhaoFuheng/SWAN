WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname, results.position,
    CASE WHEN results.time IS NOT NULL
         THEN driver_data.dob
    END AS dob
FROM driver_data
INNER JOIN results ON results.driverId = driver_data.driverId
WHERE results.raceId = 872 AND results.position <= 10
