SELECT COUNT(DISTINCT T1.superhero_name)
FROM superhero AS T1
WHERE T1.height_cm BETWEEN 160 AND 180
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero published by DC Comics? superhero_name')
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero female? superhero_name')
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero of the Human race? superhero_name')
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have the superpower Flight? superhero_name')
