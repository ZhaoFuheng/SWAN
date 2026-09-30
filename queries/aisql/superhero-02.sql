SELECT COUNT(*)
FROM superhero AS T1
WHERE ai_filter('Does this superhero have the superpower Super Strength? superhero_name: ' || T1.superhero_name)
  AND T1.height_cm > 200
