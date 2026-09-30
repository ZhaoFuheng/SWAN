SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM superhero AS S WHERE S.height_cm > 200)
FROM superhero AS T1
WHERE T1.height_cm > 200
  AND ai_filter('Is this superhero published by Marvel Comics? superhero_name: ' || T1.superhero_name)
  AND (ai_filter('Does this superhero have the superpower Super Strength? superhero_name: ' || T1.superhero_name) OR ai_filter('Does this superhero have the superpower Invulnerability? superhero_name: ' || T1.superhero_name))
