WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname
FROM driver_data
WHERE ai_filter('Is this Formula 1 driver Japanese? driver: ' || driver_data.driver)
LIMIT 5
