SELECT DISTINCT T3.attribute_name
FROM hero_attribute AS T2
INNER JOIN attribute AS T3 ON T2.attribute_id = T3.id
INNER JOIN superhero AS T1 ON T1.id = T2.hero_id
WHERE T2.attribute_value = 100
  AND T1.height_cm > 180
  AND ai_filter('Is this superhero female? superhero_name: ' || T1.superhero_name)
