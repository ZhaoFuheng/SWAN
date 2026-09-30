SELECT COUNT(*)
FROM Player
WHERE Player.weight BETWEEN 195 AND 199
  AND Player.height > 190
  AND (SUBSTR(Player.birthday, 1, 4) > '1992'
       OR SUBSTR(Player.birthday, 1, 4) < '1980')
