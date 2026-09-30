SELECT Player.player_name, pa.overall_rating, SUBSTR(Player.birthday, 1, 10) AS birthday
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE SUBSTR(pa.date, 1, 4) = '2010'
ORDER BY pa.overall_rating DESC, pa.id
LIMIT 5
