WITH heavy AS (
    SELECT superhero.superhero_name AS superhero_name,
           CASE WHEN superhero.height_cm > 200
                THEN (CASE WHEN superhero.alignment_id = (SELECT id FROM alignment WHERE alignment = 'Bad') THEN 1 ELSE 0 END)
                ELSE 0 END AS tall_and_bad
    FROM superhero
    WHERE superhero.weight_kg > 150
)
SELECT COUNT(DISTINCT heavy.superhero_name) AS heavy,
       COUNT(DISTINCT CASE WHEN heavy.tall_and_bad = 1 THEN heavy.superhero_name END) AS tall_and_bad
FROM heavy
