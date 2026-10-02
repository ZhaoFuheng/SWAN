WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname
FROM driver_data
WHERE ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Is this Formula 1 driver Japanese? driver')
LIMIT 5
