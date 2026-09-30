SELECT COUNT(T1.id)
FROM superhero AS T1
WHERE ai_filter('Does the hero has blue eye? superhero_name: ' || T1.superhero_name)
