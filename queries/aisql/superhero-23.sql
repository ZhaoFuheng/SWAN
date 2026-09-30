SELECT T1.superhero_name,
       ai_classify('What is the eye colour of this superhero? superhero_name: ' || T1.superhero_name,
                   (SELECT list(DISTINCT colour ORDER BY colour) FROM colour)) AS eye_colour
FROM superhero AS T1
WHERE T1.height_cm > 200
  AND T1.weight_kg IS NOT NULL
ORDER BY T1.weight_kg DESC, T1.id
LIMIT 5
