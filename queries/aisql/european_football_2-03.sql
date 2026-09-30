SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.player_api_id IN (SELECT pa.player_api_id FROM Player_Attributes AS pa
                                 WHERE SUBSTR(pa.date, 1, 4) = '2015' AND pa.heading_accuracy >= 80)
  AND ai_filter('Is this football player taller than 185 cm? player_name: ' || Player.player_name)
  AND ai_filter('Was this football player born in 1991 or later? player_name: ' || Player.player_name)
  AND ai_filter('Does this football player prefer his left foot? player_name: ' || Player.player_name)
