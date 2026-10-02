WITH r AS (
    SELECT DISTINCT Player.player_name, Player.weight, pa.date AS record_date, pa.overall_rating, pa.preferred_foot
    FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
    WHERE SUBSTR(pa.date, 1, 4) = '2016'
)
SELECT r.player_name, r.overall_rating, r.preferred_foot AS preferred_foot
FROM r
ORDER BY r.overall_rating DESC, r.player_name, r.weight, r.record_date
LIMIT 10
