WITH bad AS (
    SELECT T1.superhero_name AS superhero_name
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is the alignment of this superhero Bad? superhero_name')
),
bad_marvel AS (
    SELECT B.superhero_name AS superhero_name
    FROM bad AS B
    WHERE ai_filter('Context:
[superhero_name]: «' || B.superhero_name || '»


Claim: Is this superhero published by Marvel Comics? superhero_name')
)
SELECT (SELECT COUNT(DISTINCT bad.superhero_name) FROM bad) * 100.0 / (SELECT COUNT(DISTINCT S.superhero_name) FROM superhero AS S WHERE S.weight_kg > 100) AS percentage,
       (SELECT COUNT(DISTINCT bad_marvel.superhero_name) FROM bad_marvel) AS marvel
