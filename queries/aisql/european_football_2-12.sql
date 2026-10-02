SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.weight = 190
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Is this football player at least 185 cm tall? player_name')
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Was this football player born before 1985? player_name')
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Was this football player born in October? player_name')
