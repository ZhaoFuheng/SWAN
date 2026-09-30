SELECT COUNT(T1.id) 
FROM superhero AS T1
WHERE {{
    LLMMap(
        'Is the publisher DC Comics?',
        'T1::superhero_name'
    )
}} = TRUE
