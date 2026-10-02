SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.weight = 187
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Is this football player at least 193 cm tall? player_name')
LIMIT 10
