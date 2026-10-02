SELECT COUNT(DISTINCT superhero.superhero_name)
FROM superhero
WHERE superhero.weight_kg > 100
  AND (superhero.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'DC Comics') OR superhero.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics'))
  AND (superhero.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Flight') OR superhero.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Super Strength'))
