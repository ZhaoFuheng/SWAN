SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE T1.gender_id = (SELECT id FROM gender WHERE gender = 'Male')
  AND T1.eye_colour_id = (SELECT id FROM colour WHERE colour = 'Blue')
  AND T1.hair_colour_id = (SELECT id FROM colour WHERE colour = 'Blond')
