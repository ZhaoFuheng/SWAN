SELECT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Is this superhero of the Alien race? superhero_name: ' || T1.superhero_name)
LIMIT 5
