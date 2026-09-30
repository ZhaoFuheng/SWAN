SELECT COUNT(DISTINCT Player.id)
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE Player.weight < 140
  AND (pa.preferred_foot = 'left'
       OR Player.height < 170)
