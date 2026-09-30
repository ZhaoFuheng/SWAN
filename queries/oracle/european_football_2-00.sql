SELECT Player.player_name, Player.weight, ROUND(Player.height) AS height
FROM Player
WHERE Player.weight > 200
ORDER BY Player.weight DESC, Player.id
LIMIT 10
