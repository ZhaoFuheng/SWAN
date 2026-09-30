SELECT DISTINCT Player.player_name
FROM Player
WHERE Player.player_api_id IN (SELECT pa.player_api_id FROM Player_Attributes AS pa
                                 WHERE SUBSTR(pa.date, 1, 4) = '2014' AND pa.finishing >= 80)
  AND Player.height < 180
  AND Player.player_api_id IN (SELECT f.player_api_id FROM Player_Attributes AS f WHERE f.preferred_foot = 'right')
  AND SUBSTR(Player.birthday, 1, 4) < '1988'
