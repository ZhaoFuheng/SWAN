SELECT Player.player_name, pa.overall_rating,
       ai_complete('When was this football player born? player_name: ' || Player.player_name
                   || ' Answer with the date only, in YYYY-MM-DD format.') AS birthday
FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
WHERE SUBSTR(pa.date, 1, 4) = '2010'
ORDER BY pa.overall_rating DESC, pa.id
LIMIT 5
