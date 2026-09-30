SELECT {{
    LLMMap(
        'What is the race of the hero?',
        superhero.superhero_name,
        options=race.race
    )
}}
FROM superhero 
WHERE superhero.superhero_name = 'Copycat'
