SELECT COUNT(*)
FROM superhero AS T1
WHERE T1.height_cm BETWEEN 160 AND 180
  AND T1.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'DC Comics')
  AND T1.gender_id = (SELECT id FROM gender WHERE gender = 'Female')
  AND T1.race_id = (SELECT id FROM race WHERE race = 'Human')
  AND T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Flight')
