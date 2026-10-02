SELECT COUNT(DISTINCT T1.superhero_name)
FROM superhero AS T1
WHERE T1.alignment_id = (SELECT id FROM alignment WHERE alignment = 'Good')
  AND T1.publisher_id = (SELECT id FROM publisher WHERE publisher_name = 'Marvel Comics')
  AND T1.eye_colour_id = (SELECT id FROM colour WHERE colour = 'Blue')
  AND T1.id IN (SELECT hp.hero_id FROM hero_power AS hp JOIN superpower AS sp ON sp.id = hp.power_id WHERE sp.power_name = 'Flight')
