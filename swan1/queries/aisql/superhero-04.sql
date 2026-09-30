SELECT DISTINCT T1.full_name
FROM superhero AS T1
WHERE ai_filter('Does the hero has more than 15 different powers? superhero_name: ' || T1.superhero_name)
