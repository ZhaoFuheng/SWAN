SELECT COUNT(DISTINCT superhero.superhero_name)
FROM superhero
WHERE superhero.weight_kg > 100
  AND (ai_filter('Context:
[superhero_name]: «' || superhero.superhero_name || '»


Claim: Is this superhero published by DC Comics? superhero_name') OR ai_filter('Context:
[superhero_name]: «' || superhero.superhero_name || '»


Claim: Is this superhero published by Marvel Comics? superhero_name'))
  AND (ai_filter('Context:
[superhero_name]: «' || superhero.superhero_name || '»


Claim: Does this superhero have the superpower Flight? superhero_name') OR ai_filter('Context:
[superhero_name]: «' || superhero.superhero_name || '»


Claim: Does this superhero have the superpower Super Strength? superhero_name'))
