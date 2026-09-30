WITH marvel AS (
    SELECT T1.id AS id, T1.height_cm AS height_cm
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND ai_filter('Is this superhero published by Marvel Comics? superhero_name: ' || T1.superhero_name)
)
SELECT (SELECT COUNT(*) FROM marvel) AS total,
       (SELECT COUNT(*) FROM marvel WHERE marvel.height_cm > 200) AS tall
