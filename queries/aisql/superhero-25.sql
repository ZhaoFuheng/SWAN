WITH tall_female AS (
    SELECT DISTINCT T1.superhero_name AS superhero_name, T1.weight_kg AS weight_kg
    FROM superhero AS T1
    WHERE ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero female? superhero_name')
      AND T1.height_cm > 190
      AND T1.weight_kg > 0
)
SELECT AVG(tall_female.weight_kg)
FROM tall_female
