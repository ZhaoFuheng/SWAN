WITH tall_female AS (
    SELECT DISTINCT T1.superhero_name AS superhero_name, T1.weight_kg AS weight_kg
    FROM superhero AS T1
    WHERE T1.gender_id = (SELECT id FROM gender WHERE gender = 'Female')
      AND T1.height_cm > 190
      AND T1.weight_kg > 0
)
SELECT AVG(tall_female.weight_kg)
FROM tall_female
