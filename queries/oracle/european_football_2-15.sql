SELECT COUNT(DISTINCT Player.player_name || '|' || CAST(Player.weight AS VARCHAR))
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE Player.weight < 140
  AND (pa.preferred_foot = 'left'
       OR Player.height < 170)
