SELECT (SELECT race FROM race WHERE id = T1.race_id)
FROM superhero AS T1
WHERE T1.superhero_name = 'Copycat'
