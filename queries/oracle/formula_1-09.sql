WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT driver_data.forename, driver_data.surname
FROM driver_data
WHERE driver_data.dob >= '1980-01-01'
  AND driver_data.nationality = 'British'
  AND driver_data.code IS NOT NULL
