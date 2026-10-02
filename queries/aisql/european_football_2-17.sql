WITH r AS (
    SELECT DISTINCT Player.player_name, Player.weight, pa.date AS record_date, pa.overall_rating
    FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
    WHERE SUBSTR(pa.date, 1, 4) = '2010'
)
SELECT r.player_name, r.overall_rating,
       ai_complete('When was this football player born? player_name: ' || r.player_name
                   || ' Answer with the date only, in YYYY-MM-DD format.') AS birthday
FROM r
ORDER BY r.overall_rating DESC, r.player_name, r.weight, r.record_date
LIMIT 5
