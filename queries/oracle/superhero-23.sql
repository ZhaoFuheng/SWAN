SELECT T1.superhero_name,
       (SELECT colour FROM colour WHERE id = T1.eye_colour_id) AS eye_colour
FROM (SELECT DISTINCT S.superhero_name AS superhero_name, S.weight_kg AS weight_kg, S.eye_colour_id AS eye_colour_id
      FROM superhero AS S
      WHERE S.height_cm > 200
        AND S.weight_kg IS NOT NULL) AS T1
ORDER BY T1.weight_kg DESC, T1.superhero_name
LIMIT 5
