SELECT T1.superhero_name,
       (SELECT colour FROM colour WHERE id = T1.eye_colour_id) AS eye_colour
FROM superhero AS T1
WHERE T1.height_cm > 200
  AND T1.weight_kg IS NOT NULL
ORDER BY T1.weight_kg DESC, T1.id
LIMIT 5
