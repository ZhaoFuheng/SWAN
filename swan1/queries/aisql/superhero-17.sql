SELECT ai_classify('What is the race of the hero? superhero_name: ' || superhero.superhero_name,
                   (SELECT list(DISTINCT race ORDER BY race) FROM race))
FROM superhero
WHERE superhero.superhero_name = 'Copycat'
