SELECT T1.superhero_name 
    FROM superhero AS T1
    WHERE {{
        LLMMap(
        'Does the hero has blue eye?',
        T1.superhero_name
        )
    }} = TRUE AND {{
        LLMMap(
        'Does the hero has blond hair?',
        T1.superhero_name
        )
    }} = TRUE
