SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.player_api_id IN (SELECT pa.player_api_id FROM Player_Attributes AS pa
                                 WHERE SUBSTR(pa.date, 1, 4) = '2014' AND pa.finishing >= 80)
  AND ai_filter('Is this football player shorter than 180 cm? player_name: ' || Player.player_name)
  AND ai_filter('Does this football player prefer his right foot? player_name: ' || Player.player_name)
  AND ai_filter('Was this football player born before 1988? player_name: ' || Player.player_name)
