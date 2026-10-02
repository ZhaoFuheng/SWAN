SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Death Touch')
LIMIT 3
