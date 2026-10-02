WITH r AS (
    SELECT DISTINCT Player.player_name, Player.weight, pa.date AS record_date, pa.crossing
    FROM Player INNER JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
    WHERE SUBSTR(pa.date, 1, 4) = '2016'
      AND pa.overall_rating >= 75
)
SELECT 100.0 * SUM(CASE WHEN r.crossing >= 75
                        THEN CASE WHEN ai_classify('Which foot does this football player prefer? player_name: ' || r.player_name, ['left', 'right']) = 'left' THEN 1 ELSE 0 END
                        ELSE 0 END) / COUNT(*) AS percentage
FROM r
