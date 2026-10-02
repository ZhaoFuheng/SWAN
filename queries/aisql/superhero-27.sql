SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero of the Alien race? superhero_name')
LIMIT 5
