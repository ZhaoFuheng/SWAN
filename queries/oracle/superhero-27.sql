SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE T1.race_id = (SELECT id FROM race WHERE race = 'Alien')
LIMIT 5
