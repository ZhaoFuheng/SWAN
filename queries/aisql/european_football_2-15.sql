SELECT COUNT(DISTINCT Player.id)
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE Player.weight < 140
  AND (ai_filter('Does this football player prefer his left foot? player_name: ' || Player.player_name)
       OR ai_filter('Is this football player shorter than 170 cm? player_name: ' || Player.player_name))
