SELECT AVG(T1.height_cm)
FROM superhero AS T1
WHERE ai_filter('Is the publisher Marvel Comics? superhero_name: ' || T1.superhero_name)
