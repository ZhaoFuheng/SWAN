SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE T1.eye_colour_id = (SELECT id FROM colour WHERE colour = 'Brown')
  AND T1.height_cm BETWEEN 170 AND 175
