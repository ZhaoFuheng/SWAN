SELECT T1.superhero_name,
       ai_classify('Does this superhero have the superpower Super Strength? superhero_name: ' || T1.superhero_name,
                   ['Yes', 'No']) AS super_strength
FROM superhero AS T1
INNER JOIN (SELECT T.hero_id AS hero_id, SUM(T.attribute_value) AS total
            FROM hero_attribute AS T
            GROUP BY T.hero_id) AS T2 ON T1.id = T2.hero_id
ORDER BY T2.total DESC, T1.id
LIMIT 5
