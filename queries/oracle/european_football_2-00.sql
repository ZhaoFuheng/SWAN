WITH p AS (
    SELECT DISTINCT Player.player_name, Player.weight, Player.height
    FROM Player
    WHERE Player.weight > 200
)
SELECT p.player_name, p.weight, ROUND(p.height) AS height
FROM p
ORDER BY p.weight DESC, p.player_name
LIMIT 10
