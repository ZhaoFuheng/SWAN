SELECT COUNT(T1.id)
FROM superhero AS T1
WHERE ai_filter('Is the publisher DC Comics? superhero_name: ' || T1.superhero_name)
