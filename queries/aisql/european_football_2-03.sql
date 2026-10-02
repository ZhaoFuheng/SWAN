SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.player_api_id IN (SELECT pa.player_api_id FROM Player_Attributes AS pa
                                 WHERE SUBSTR(pa.date, 1, 4) = '2015' AND pa.heading_accuracy >= 80)
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Is this football player at least 185 cm tall? player_name')
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Was this football player born in 1991 or later? player_name')
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Does this football player prefer his left foot? player_name')
