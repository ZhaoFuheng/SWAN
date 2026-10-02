SELECT T1.superhero_name, T1.full_name,
       (SELECT publisher_name FROM publisher WHERE id = T1.publisher_id) AS publisher
FROM (SELECT DISTINCT S.superhero_name AS superhero_name, S.full_name AS full_name, S.height_cm AS height_cm, S.publisher_id AS publisher_id
      FROM superhero AS S
      WHERE S.weight_kg BETWEEN 100 AND 200
        AND S.height_cm IS NOT NULL) AS T1
ORDER BY T1.height_cm DESC, T1.superhero_name
LIMIT 5
