SELECT COUNT(DISTINCT T1.superhero_name) * 100.0 / (SELECT COUNT(DISTINCT S.superhero_name) FROM superhero AS S WHERE S.height_cm > 200)
FROM superhero AS T1
WHERE T1.height_cm > 200
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero published by Marvel Comics? superhero_name')
  AND (ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have the superpower Super Strength? superhero_name') OR ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have the superpower Invulnerability? superhero_name'))
