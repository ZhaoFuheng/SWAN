SELECT T1.power_name
FROM superpower AS T1
WHERE ai_filter('Context:
[power_name]: «' || T1.power_name || '»


Claim: Does the superhero Deathlok have this superpower? power_name')
