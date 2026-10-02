WITH p AS (
    SELECT DISTINCT Player.player_name, Player.weight
    FROM Player
    WHERE Player.weight > 200
)
SELECT p.player_name, p.weight,
       TRY_CAST(ai_complete('What is the height of this football player in centimetres, rounded to a whole number? player_name: ' || p.player_name || ' Answer with the number only.') AS DOUBLE) AS height
FROM p
ORDER BY p.weight DESC, p.player_name
LIMIT 10
