WITH driver_data AS (
    SELECT *, drivers.forename || ' ' || drivers.surname AS driver
    FROM drivers
)
SELECT DISTINCT driver_data.forename, driver_data.surname
FROM driver_data
WHERE ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Was this Formula 1 driver born in 1980 or later? driver')
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Is this Formula 1 driver British? driver')
  AND ai_filter('Context:
[driver]: «' || driver_data.driver || '»


Claim: Does this Formula 1 driver have an official three-letter driver code? driver')
