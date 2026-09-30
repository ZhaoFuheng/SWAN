SELECT Player.player_name
FROM Player
WHERE Player.weight = 187
  AND ai_filter('Is this football player taller than 193 cm? player_name: ' || Player.player_name)
LIMIT 10
