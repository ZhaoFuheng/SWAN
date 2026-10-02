SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE T1.height_cm > 180
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have blue eyes? superhero_name')
LIMIT 10
