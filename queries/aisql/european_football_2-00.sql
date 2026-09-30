SELECT Player.player_name, Player.weight,
       TRY_CAST(ai_complete('What is the height of this football player in centimetres, rounded to a whole number? player_name: ' || Player.player_name || ' Answer with the number only.') AS DOUBLE) AS height
FROM Player
WHERE Player.weight > 200
ORDER BY Player.weight DESC, Player.id
LIMIT 10
