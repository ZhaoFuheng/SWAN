SELECT T1.superhero_name
FROM superhero AS T1
WHERE T1.height_cm > 180
  AND T1.eye_colour_id = (SELECT id FROM colour WHERE colour = 'Blue')
LIMIT 10
