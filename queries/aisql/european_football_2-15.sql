SELECT COUNT(DISTINCT Player.player_name || '|' || CAST(Player.weight AS VARCHAR))
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE Player.weight < 140
  AND (ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Does this football player prefer his left foot? player_name')
       OR ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Is this football player shorter than 170 cm? player_name'))
