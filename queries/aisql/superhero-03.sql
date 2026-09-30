SELECT T1.superhero_name
FROM superhero AS T1
WHERE T1.height_cm > 180
  AND ai_filter('Does this superhero have blue eyes? superhero_name: ' || T1.superhero_name)
LIMIT 10
