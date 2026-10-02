SELECT DISTINCT T1.superhero_name
FROM superhero AS T1
WHERE ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Is this superhero male? superhero_name')
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have blue eyes? superhero_name')
  AND ai_filter('Context:
[superhero_name]: «' || T1.superhero_name || '»


Claim: Does this superhero have blond hair? superhero_name')
