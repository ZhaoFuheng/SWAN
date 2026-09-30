SELECT ai_classify('Provide the eye color. superhero_name: ' || superhero.superhero_name,
                   (SELECT list(DISTINCT colour ORDER BY colour) FROM colour))
FROM superhero
WHERE id = 75
