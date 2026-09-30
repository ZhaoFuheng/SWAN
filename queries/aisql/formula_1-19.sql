WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname,
    ai_complete('What is the three-letter abbreviated code of this Formula 1 driver? driver: ' || driver_data.driver
                || ' Answer with the value only, without any other words.') AS code
FROM driver_data
WHERE driver_data.driverId IN (SELECT qualifying.driverId FROM qualifying
                               INNER JOIN races ON races.raceId = qualifying.raceId WHERE races.year = 2016)
  AND (ai_filter('Is this Formula 1 driver Finnish? driver: ' || driver_data.driver)
       OR ai_filter('Is this Formula 1 driver Danish? driver: ' || driver_data.driver))
