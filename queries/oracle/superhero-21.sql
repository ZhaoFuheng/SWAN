WITH bad AS (
    SELECT T1.id AS id, T1.superhero_name AS superhero_name, T1.publisher_id AS publisher_id
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND T1.alignment_id = (SELECT id FROM alignment WHERE alignment = 'Bad')
),
bad_marvel AS (
    SELECT B.id AS id
    FROM bad AS B
    WHERE B.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
)
SELECT (SELECT COUNT(*) FROM bad) * 100.0 / (SELECT COUNT(*) FROM superhero AS S WHERE S.weight_kg > 100) AS percentage,
       (SELECT COUNT(*) FROM bad_marvel) AS marvel
