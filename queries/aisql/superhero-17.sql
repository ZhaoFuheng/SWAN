SELECT DISTINCT ai_classify('What is the race of this superhero? superhero_name: ' || T1.superhero_name,
                   (SELECT list(DISTINCT race ORDER BY race) FROM race))
FROM superhero AS T1
WHERE T1.superhero_name = 'Copycat'
