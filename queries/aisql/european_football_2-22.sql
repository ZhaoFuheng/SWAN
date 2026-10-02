SELECT COUNT(DISTINCT Player.player_name || '|' || CAST(Player.weight AS VARCHAR))
FROM Player
WHERE Player.weight BETWEEN 195 AND 199
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Is this football player at least 190 cm tall? player_name')
  AND (ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Was this football player born after 1992? player_name')
       OR ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Was this football player born before 1980? player_name'))
