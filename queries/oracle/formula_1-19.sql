WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname, driver_data.code AS code
FROM driver_data
WHERE driver_data.driverId IN (SELECT qualifying.driverId FROM qualifying
                               INNER JOIN races ON races.raceId = qualifying.raceId WHERE races.year = 2016)
  AND (driver_data.nationality = 'Finnish'
       OR driver_data.nationality = 'Danish')
