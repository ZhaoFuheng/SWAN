WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname
FROM results
INNER JOIN driver_data ON driver_data.driverId = results.driverId
WHERE results.raceId = 872 AND results.time IS NOT NULL
  AND driver_data.nationality IN ('British', 'German', 'French', 'Spanish', 'Finnish', 'Italian', 'Belgian', 'Dutch', 'Swiss', 'Russian', 'Danish', 'Swedish', 'Austrian', 'Polish', 'Portuguese')
  AND driver_data.dob >= '1985-01-01'
  AND driver_data.nationality <> 'German'
