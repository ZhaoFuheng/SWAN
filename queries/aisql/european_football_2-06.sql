SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.player_api_id IN (SELECT pa.player_api_id FROM Player_Attributes AS pa
                                 WHERE SUBSTR(pa.date, 1, 4) BETWEEN '2013' AND '2015' AND pa.sprint_speed >= 93)
  AND ai_filter('Was this football player born before 1990? player_name: ' || Player.player_name)
LIMIT 5
