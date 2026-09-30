SELECT T1.full_name
FROM superhero AS T1
WHERE ai_filter('Is the publisher Marvel Comics? superhero_name: ' || T1.superhero_name)
ORDER BY T1.height_cm DESC
LIMIT 1
