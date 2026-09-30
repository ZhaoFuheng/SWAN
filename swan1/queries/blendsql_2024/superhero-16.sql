SELECT COUNT(T1.id) 
FROM superhero AS T1
WHERE {{
    LLMMap(
        'Is the publisher Marvel Comics?',
        'T1::superhero_name'
    )
}} = TRUE AND {{
    LLMMap(
        'Does the hero has gold eye?',
        'T1::superhero_name'
    )
}} = TRUE
