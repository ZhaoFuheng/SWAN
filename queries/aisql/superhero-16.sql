SELECT COUNT(*)
FROM superhero AS T1
WHERE T1.weight_kg > 80
  AND ai_filter('Is this superhero male? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Is this superhero published by Marvel Comics? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does this superhero have yellow eyes? superhero_name: ' || T1.superhero_name)
  AND ai_filter('Does this superhero have the superpower Super Strength? superhero_name: ' || T1.superhero_name)
