SELECT T1.power_name
FROM superpower AS T1
WHERE T1.id IN (SELECT hp.power_id FROM hero_power AS hp JOIN superhero AS s ON s.id = hp.hero_id
                WHERE s.superhero_name = 'Deathlok')
