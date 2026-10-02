SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have brown eyes? superhero_name')
  AND T1.height_cm BETWEEN 170 AND 175
