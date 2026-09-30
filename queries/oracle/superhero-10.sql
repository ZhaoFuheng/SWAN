SELECT T1.superhero_name, T1.full_name,
       (SELECT publisher_name FROM publisher WHERE id = T1.publisher_id) AS publisher
FROM superhero AS T1
WHERE T1.weight_kg BETWEEN 100 AND 200
  AND T1.height_cm IS NOT NULL
ORDER BY T1.height_cm DESC, T1.id
LIMIT 5
