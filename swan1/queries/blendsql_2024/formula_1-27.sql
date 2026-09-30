WITH driver_data AS (
SELECT T1.driverId, T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key
FROM drivers AS T1
), temp AS (
SELECT *,{{
    LLMMap(
    'Provide the date of birth.',
    'driver_data::key'
    )
}} AS dob
from driver_data
)
SELECT STRFTIME('%Y', CURRENT_TIMESTAMP) - STRFTIME('%Y', dob), forename, surname 
FROM temp
WHERE {{
    LLMMap(
        'Provide the nationality.',
        'temp::key'
    )
}} = 'Japanese'
ORDER BY dob 
DESC LIMIT 8
