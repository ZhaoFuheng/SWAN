SELECT COUNT(T1.superhero_name)
FROM superhero AS T1
WHERE ai_classify('Provide the race. superhero_name: ' || T1.superhero_name,
                  (SELECT list(DISTINCT race ORDER BY race) FROM race)) = 'Vampire'
