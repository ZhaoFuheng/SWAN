WITH bad AS (
    SELECT T1.superhero_name AS superhero_name, T1.publisher_id AS publisher_id
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND T1.alignment_id = (SELECT id FROM alignment WHERE alignment = 'Bad')
),
bad_marvel AS (
    SELECT B.superhero_name AS superhero_name
    FROM bad AS B
    WHERE B.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
)
SELECT (SELECT COUNT(DISTINCT bad.superhero_name) FROM bad) * 100.0 / (SELECT COUNT(DISTINCT S.superhero_name) FROM superhero AS S WHERE S.weight_kg > 100) AS percentage,
       (SELECT COUNT(DISTINCT bad_marvel.superhero_name) FROM bad_marvel) AS marvel
