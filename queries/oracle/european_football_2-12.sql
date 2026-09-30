SELECT Player.player_name
FROM Player
WHERE Player.weight = 190
  AND Player.height > 185
  AND SUBSTR(Player.birthday, 1, 4) < '1985'
  AND SUBSTR(Player.birthday, 6, 2) = '10'
