SELECT COUNT(*)
FROM superhero AS T1
WHERE T1.eye_colour_id = (SELECT id FROM colour WHERE colour = 'Blue')
  AND T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Agility')
  AND T1.gender_id = (SELECT id FROM gender WHERE gender = 'Male')
  AND T1.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
