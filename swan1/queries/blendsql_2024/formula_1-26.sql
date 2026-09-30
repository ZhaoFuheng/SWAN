WITH driver_data AS (
    SELECT T1.driverId, T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key
    FROM drivers AS T1
)
SELECT  driver_data.forename, driver_data.surname, {{
        LLMMap(
            'Provide the nationality.',
            'driver_data::key'
        )
    }} AS nationality,
    AVG(T2.points) AS avg_points
FROM driver_data
INNER JOIN driverStandings AS T2 ON T2.driverId = driver_data.driverId
WHERE T2.wins = 1
GROUP BY driver_data.forename, driver_data.surname, nationality
ORDER BY COUNT(T2.wins) DESC
LIMIT 10
