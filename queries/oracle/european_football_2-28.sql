SELECT AVG(pa.overall_rating)
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE SUBSTR(pa.date, 1, 4) = '2010'
  AND Player.height > 190
