WITH r AS (
    SELECT DISTINCT Player.player_name, Player.weight, pa.date AS record_date, pa.overall_rating, Player.birthday
    FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
    WHERE SUBSTR(pa.date, 1, 4) = '2010'
)
SELECT r.player_name, r.overall_rating, SUBSTR(r.birthday, 1, 10) AS birthday
FROM r
ORDER BY r.overall_rating DESC, r.player_name, r.weight, r.record_date
LIMIT 5
