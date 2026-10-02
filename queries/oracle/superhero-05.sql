SELECT DISTINCT (SELECT colour FROM colour WHERE id = T1.skin_colour_id)
FROM superhero AS T1
WHERE T1.superhero_name = 'Apocalypse'
