SELECT T1.superhero_name,
       ai_classify('What is the eye colour of this superhero? superhero_name: ' || T1.superhero_name,
                   (SELECT list(DISTINCT colour ORDER BY colour) FROM colour)) AS eye_colour
FROM (SELECT DISTINCT S.superhero_name AS superhero_name, S.weight_kg AS weight_kg
      FROM superhero AS S
      WHERE S.height_cm > 200
        AND S.weight_kg IS NOT NULL) AS T1
ORDER BY T1.weight_kg DESC, T1.superhero_name
LIMIT 5
