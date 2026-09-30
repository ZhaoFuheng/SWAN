SELECT superhero.superhero_name,
       CASE WHEN superhero.weight_kg >= 200
            THEN (CASE WHEN superhero.race_id = (SELECT id FROM race WHERE race = 'Zombie') THEN 1 ELSE 0 END)
            END AS zombie
FROM superhero
WHERE superhero.height_cm >= 250
