SELECT T1.superhero_name 
    FROM superhero AS T1
    WHERE {{
        LLMMap(
            'Is the race of the hero Alien?',
            T1.superhero_name
        )
    }} = TRUE
