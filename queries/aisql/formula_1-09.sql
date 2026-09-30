WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname
FROM driver_data
WHERE ai_filter('Was this Formula 1 driver born in 1980 or later? driver: ' || driver_data.driver)
  AND ai_filter('Is this Formula 1 driver British? driver: ' || driver_data.driver)
  AND ai_filter('Does this Formula 1 driver have an official three-letter driver code? driver: ' || driver_data.driver)
