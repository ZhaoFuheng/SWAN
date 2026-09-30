SELECT T3.attribute_name, AVG(T2.attribute_value)
FROM superhero AS T1
INNER JOIN hero_attribute AS T2 ON T1.id = T2.hero_id
INNER JOIN attribute AS T3 ON T2.attribute_id = T3.id
WHERE T1.height_cm > 200
  AND T1.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
GROUP BY T3.attribute_name
