WITH p AS (
    SELECT DISTINCT Player.player_name, Player.weight
    FROM Player
    WHERE Player.weight >= 200
),
grp AS (
    SELECT p.player_name,
           TRY_CAST(ai_complete('What is the height of this football player in centimetres? player_name: ' || p.player_name
                                || ' Answer with the number only.') AS DOUBLE) AS height
    FROM p
    WHERE ai_filter('Context:
[player_name]: «' || p.player_name || '»


Claim: Was this football player born between 1990 and 1995? player_name')
)
SELECT COUNT(*)
FROM grp
WHERE grp.height > (SELECT AVG(g2.height) FROM grp AS g2)
