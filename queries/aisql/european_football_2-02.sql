WITH grp AS (
    SELECT Player.player_name,
           TRY_CAST(ai_complete('What is the height of this football player in centimetres? player_name: ' || Player.player_name
                                || ' Answer with the number only.') AS DOUBLE) AS height
    FROM Player
    WHERE Player.weight >= 200
      AND ai_filter('Was this football player born between 1990 and 1995? player_name: ' || Player.player_name)
)
SELECT COUNT(*)
FROM grp
WHERE grp.height > (SELECT AVG(g2.height) FROM grp AS g2)
