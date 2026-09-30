SELECT COUNT(*)
FROM superhero
WHERE superhero.weight_kg > 100
  AND (ai_filter('Is this superhero published by DC Comics? superhero_name: ' || superhero.superhero_name) OR ai_filter('Is this superhero published by Marvel Comics? superhero_name: ' || superhero.superhero_name))
  AND (ai_filter('Does this superhero have the superpower Flight? superhero_name: ' || superhero.superhero_name) OR ai_filter('Does this superhero have the superpower Super Strength? superhero_name: ' || superhero.superhero_name))
