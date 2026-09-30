WITH driver_data AS (
    SELECT T1.driverId, T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key
    FROM drivers AS T1
), temp_cte AS (
    SELECT *,
        TRY_CAST(ai_complete('Provide the date of birth. key: ' || driver_data.key
                             || ' Answer with the date only, in YYYY-MM-DD format.') AS DATE) AS dob
    FROM driver_data
)
SELECT CAST(strftime(CURRENT_TIMESTAMP, '%Y') AS BIGINT) - year(dob), forename, surname
FROM temp_cte
WHERE trim(ai_complete('Provide the nationality. key: ' || temp_cte.key || ' Answer with the value only, without any other words.')) = 'Japanese'
ORDER BY dob DESC NULLS LAST
LIMIT 8
