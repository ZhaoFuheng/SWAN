SELECT COUNT(DISTINCT Player.player_name || '|' || CAST(Player.weight AS VARCHAR))
FROM Player
WHERE Player.weight BETWEEN 195 AND 199
  AND Player.height >= 190
  AND (SUBSTR(Player.birthday, 1, 4) > '1992'
       OR SUBSTR(Player.birthday, 1, 4) < '1980')
