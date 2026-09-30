SELECT COUNT(T1.id)
FROM superhero AS T1
WHERE ai_filter('Is the publisher Marvel Comics? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does the hero has gold eye? superhero_name: ' || T1.superhero_name)
