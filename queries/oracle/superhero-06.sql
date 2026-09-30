WITH marvel AS (
    SELECT T1.id AS id, T1.height_cm AS height_cm
    FROM superhero AS T1
    WHERE T1.weight_kg > 100
      AND T1.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
)
SELECT (SELECT COUNT(*) FROM marvel) AS total,
       (SELECT COUNT(*) FROM marvel WHERE marvel.height_cm > 200) AS tall
