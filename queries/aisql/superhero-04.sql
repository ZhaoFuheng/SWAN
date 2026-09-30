SELECT T1.superhero_name
FROM superhero AS T1
INNER JOIN hero_attribute AS T2 ON T1.id = T2.hero_id
WHERE T2.attribute_value = 100
  AND ai_filter('Does this superhero have the superpower Telepathy? superhero_name: ' || T1.superhero_name)
GROUP BY T1.id, T1.superhero_name
HAVING COUNT(*) >= 3
