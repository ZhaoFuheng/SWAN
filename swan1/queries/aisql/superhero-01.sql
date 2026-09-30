SELECT COUNT(T1.superhero_name)
FROM superhero AS T1
WHERE ai_filter('Does the hero has Super Strength? superhero_name: ' || T1.superhero_name)
