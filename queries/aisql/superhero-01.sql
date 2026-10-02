SELECT COUNT(DISTINCT T1.superhero_name || '|' || T2.attribute_id)
FROM hero_attribute AS T2
INNER JOIN superhero AS T1 ON T1.id = T2.hero_id
WHERE T2.attribute_value = 100
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have the superpower Super Strength? superhero_name')
