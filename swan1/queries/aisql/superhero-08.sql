SELECT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Does the hero has blue eye? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does the hero has blond hair? superhero_name: ' || T1.superhero_name)
