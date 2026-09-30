SELECT COUNT(*)
FROM hero_attribute AS T2
INNER JOIN superhero AS T1 ON T1.id = T2.hero_id
WHERE T2.attribute_value = 100
  AND ai_filter('Does this superhero have the superpower Super Strength? superhero_name: ' || T1.superhero_name)
