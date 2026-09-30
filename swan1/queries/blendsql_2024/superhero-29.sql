SELECT COUNT(T1.id) 
    FROM superhero AS T1
    WHERE {{
        LLMMap(
            'Is the hero bad?',
            'T1::superhero_name'
        )
    }} = TRUE
