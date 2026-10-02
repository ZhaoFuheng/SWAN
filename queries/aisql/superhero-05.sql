SELECT DISTINCT ai_classify('What is the skin colour of this superhero? superhero_name: ' || T1.superhero_name,
                   (SELECT list(DISTINCT colour ORDER BY colour) FROM colour))
FROM superhero AS T1
WHERE T1.superhero_name = 'Apocalypse'
