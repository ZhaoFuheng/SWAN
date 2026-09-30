SELECT COUNT(*)
FROM superhero AS T1
WHERE ai_filter('Is the alignment of this superhero Good? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Is this superhero published by Marvel Comics? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does this superhero have blue eyes? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does this superhero have the superpower Flight? superhero_name: ' || T1.superhero_name)
