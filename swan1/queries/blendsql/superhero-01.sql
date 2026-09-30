SELECT COUNT(T1.superhero_name) 
    FROM superhero AS T1 
    WHERE {{
        LLMMap(
            'Does the hero has Super Strength?',
            T1.superhero_name
        )
    }} = TRUE
