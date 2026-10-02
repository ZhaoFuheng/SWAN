SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.player_api_id IN (SELECT pa.player_api_id FROM Player_Attributes AS pa
                                 WHERE SUBSTR(pa.date, 1, 4) = '2014' AND pa.overall_rating >= 80)
  AND ai_filter('Context:
[player_name]: «' || Player.player_name || '»


Claim: Does this football player prefer his left foot? player_name')
LIMIT 5
