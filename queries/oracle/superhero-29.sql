SELECT COUNT(*) AS heavy,
       SUM(CASE WHEN superhero.height_cm > 200
                THEN (CASE WHEN superhero.alignment_id = (SELECT id FROM alignment WHERE alignment = 'Bad') THEN 1 ELSE 0 END)
                ELSE 0 END) AS tall_and_bad
FROM superhero
WHERE superhero.weight_kg > 150
