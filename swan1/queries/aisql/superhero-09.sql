SELECT ai_classify('Provide the publisher. superhero_name: ' || superhero.superhero_name,
                   (SELECT list(DISTINCT publisher_name ORDER BY publisher_name) FROM publisher))
FROM superhero
WHERE superhero.superhero_name = 'Blue Beetle II'
