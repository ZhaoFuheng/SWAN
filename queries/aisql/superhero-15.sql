SELECT COUNT(*)
FROM superhero AS T1
WHERE T1.height_cm BETWEEN 160 AND 180
  AND ai_filter('Is this superhero published by DC Comics? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Is this superhero female? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Is this superhero of the Human race? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does this superhero have the superpower Flight? superhero_name: ' || T1.superhero_name)
