SELECT T1.superhero_name,
       CASE WHEN T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Super Strength') THEN 'Yes' ELSE 'No' END AS super_strength
FROM superhero AS T1
INNER JOIN (SELECT T.hero_id AS hero_id, SUM(T.attribute_value) AS total
            FROM hero_attribute AS T
            GROUP BY T.hero_id) AS T2 ON T1.id = T2.hero_id
ORDER BY T2.total DESC, T1.id
LIMIT 5
