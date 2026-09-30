WITH grp AS (
    SELECT Player.player_name, Player.height AS height
    FROM Player
    WHERE Player.weight >= 200
      AND SUBSTR(Player.birthday, 1, 4) BETWEEN '1990' AND '1995'
)
SELECT COUNT(*)
FROM grp
WHERE grp.height > (SELECT AVG(g2.height) FROM grp AS g2)
