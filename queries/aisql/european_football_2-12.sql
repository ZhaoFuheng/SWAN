SELECT Player.player_name
FROM Player
WHERE Player.weight = 190
  AND ai_filter('Is this football player taller than 185 cm? player_name: ' || Player.player_name)
  AND ai_filter('Was this football player born before 1985? player_name: ' || Player.player_name)
  AND ai_filter('Was this football player born in October? player_name: ' || Player.player_name)
