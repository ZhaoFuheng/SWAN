SELECT COUNT(*)
FROM Player
WHERE Player.weight BETWEEN 195 AND 199
  AND ai_filter('Is this football player taller than 190 cm? player_name: ' || Player.player_name)
  AND (ai_filter('Was this football player born after 1992? player_name: ' || Player.player_name)
       OR ai_filter('Was this football player born before 1980? player_name: ' || Player.player_name))
