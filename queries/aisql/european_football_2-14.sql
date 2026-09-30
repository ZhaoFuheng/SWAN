SELECT Player.player_name, pa.overall_rating, ai_classify('Which foot does this football player prefer? player_name: ' || Player.player_name, ['left', 'right']) AS preferred_foot
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE SUBSTR(pa.date, 1, 4) = '2016'
ORDER BY pa.overall_rating DESC, pa.id
LIMIT 10
