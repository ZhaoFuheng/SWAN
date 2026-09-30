SELECT AVG(T1.weight_kg) 
    FROM superhero AS T1
    WHERE {{
        LLMMap(
            'Is the hero female?',
            T1.superhero_name
        )
    }} = TRUE
