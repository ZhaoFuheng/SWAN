WITH marvel AS (
    SELECT T1.superhero_name AS superhero_name, T1.height_cm AS height_cm
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero published by Marvel Comics? superhero_name')
)
SELECT (SELECT COUNT(DISTINCT marvel.superhero_name) FROM marvel) AS total,
       (SELECT COUNT(DISTINCT marvel.superhero_name) FROM marvel WHERE marvel.height_cm > 200) AS tall
