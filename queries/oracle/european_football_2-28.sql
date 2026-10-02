WITH r AS (
    SELECT DISTINCT Player.player_name, Player.weight, pa.date AS record_date, pa.overall_rating, Player.height
    FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
    WHERE SUBSTR(pa.date, 1, 4) = '2010'
)
SELECT AVG(r.overall_rating)
FROM r
WHERE r.height >= 190
