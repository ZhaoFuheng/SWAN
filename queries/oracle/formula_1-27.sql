WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname
FROM driver_data
WHERE driver_data.nationality = 'Japanese'
LIMIT 5
