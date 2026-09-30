SELECT AVG(T1.weight_kg)
FROM superhero AS T1
WHERE ai_filter('Is this superhero female? superhero_name: ' || T1.superhero_name)
  AND T1.height_cm > 190
