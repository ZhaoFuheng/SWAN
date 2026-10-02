SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.weight < 130
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Is this football player shorter than 170 cm? player_name')
