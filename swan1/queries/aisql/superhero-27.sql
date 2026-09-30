SELECT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Is the race of the hero Alien? superhero_name: ' || T1.superhero_name)
