SELECT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Does this superhero have the superpower Death Touch? superhero_name: ' || T1.superhero_name)
LIMIT 3
