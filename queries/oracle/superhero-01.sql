SELECT COUNT(*)
FROM hero_attribute AS T2
INNER JOIN superhero AS T1 ON T1.id = T2.hero_id
WHERE T2.attribute_value = 100
  AND T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Super Strength')
