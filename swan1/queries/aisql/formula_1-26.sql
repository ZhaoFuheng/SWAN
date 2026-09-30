WITH driver_data AS (
    SELECT T1.driverId, T1.forename, T1.surname, T1.forename || ' ' || T1.surname AS key
    FROM drivers AS T1
), rows AS (
    SELECT driver_data.forename, driver_data.surname,
        ai_complete('Provide the nationality. key: ' || driver_data.key || ' Answer with the value only, without any other words.') AS nationality,
        T2.points, T2.wins
    FROM driver_data
    INNER JOIN driverStandings AS T2 ON T2.driverId = driver_data.driverId
    WHERE T2.wins = 1
)
SELECT forename, surname, nationality, AVG(points) AS avg_points
FROM rows
GROUP BY forename, surname, nationality
ORDER BY COUNT(wins) DESC
LIMIT 10
