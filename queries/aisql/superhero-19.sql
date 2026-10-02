SELECT T1.superhero_name,
       ai_classify('Does this superhero have the superpower Super Strength? superhero_name: ' || T1.superhero_name,
                   ['Yes', 'No']) AS super_strength
FROM (SELECT DISTINCT S.superhero_name AS superhero_name, T2.total AS total
      FROM superhero AS S
      INNER JOIN (SELECT T.hero_id AS hero_id, SUM(T.attribute_value) AS total
                  FROM hero_attribute AS T
                  GROUP BY T.hero_id) AS T2 ON S.id = T2.hero_id) AS T1
ORDER BY T1.total DESC, T1.superhero_name
LIMIT 5
