SELECT COUNT(T1.id)
FROM superhero AS T1
WHERE T1.height_cm > 200
  AND ai_filter('Does the hero has Super Strength? superhero_name: ' || T1.superhero_name)
