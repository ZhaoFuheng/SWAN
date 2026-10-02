SELECT COUNT(DISTINCT T1.superhero_name) * 100.0 / (SELECT COUNT(DISTINCT S.superhero_name) FROM superhero AS S WHERE S.height_cm > 200)
FROM superhero AS T1
WHERE T1.height_cm > 200
  AND T1.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
  AND (T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Super Strength') OR T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Invulnerability'))
