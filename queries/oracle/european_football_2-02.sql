WITH p AS (
    SELECT DISTINCT Player.player_name, Player.weight, Player.height, Player.birthday
    FROM Player
    WHERE Player.weight >= 200
),
grp AS (
    SELECT p.player_name, p.height AS height
    FROM p
    WHERE SUBSTR(p.birthday, 1, 4) BETWEEN '1990' AND '1995'
)
SELECT COUNT(*)
FROM grp
WHERE grp.height > (SELECT AVG(g2.height) FROM grp AS g2)
