SELECT DISTINCT (SELECT publisher_name FROM publisher WHERE id = T1.publisher_id)
FROM superhero AS T1
WHERE T1.superhero_name = 'Sauron'
