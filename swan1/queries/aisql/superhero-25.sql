SELECT AVG(T1.weight_kg)
FROM superhero AS T1
WHERE ai_filter('Is the hero female? superhero_name: ' || T1.superhero_name)
