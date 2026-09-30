SELECT COUNT(*) AS heavy,
       SUM(CASE WHEN superhero.height_cm > 200
                THEN (CASE WHEN ai_filter('Is the alignment of this superhero Bad? superhero_name: ' || superhero.superhero_name) THEN 1 ELSE 0 END)
                ELSE 0 END) AS tall_and_bad
FROM superhero
WHERE superhero.weight_kg > 150
