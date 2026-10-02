SELECT DISTINCT superhero.superhero_name,
       CASE WHEN superhero.weight_kg >= 200
            THEN (CASE WHEN ai_filter('Context:
[superhero_name]: «' || superhero.superhero_name || '»


Claim: Is this superhero of the Zombie race? superhero_name') THEN 1 ELSE 0 END)
            END AS zombie
FROM superhero
WHERE superhero.height_cm >= 250
