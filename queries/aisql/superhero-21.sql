WITH bad AS (
    SELECT T1.id AS id, T1.superhero_name AS superhero_name
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND ai_filter('Is the alignment of this superhero Bad? superhero_name: ' || T1.superhero_name)
),
bad_marvel AS (
    SELECT B.id AS id
    FROM bad AS B
    WHERE ai_filter('Is this superhero published by Marvel Comics? superhero_name: ' || B.superhero_name)
)
SELECT (SELECT COUNT(*) FROM bad) * 100.0 / (SELECT COUNT(*) FROM superhero AS S WHERE S.weight_kg > 100) AS percentage,
       (SELECT COUNT(*) FROM bad_marvel) AS marvel
