SELECT AVG(T1.weight_kg)
FROM superhero AS T1
WHERE T1.gender_id = (SELECT id FROM gender WHERE gender = 'Female')
  AND T1.height_cm > 190
