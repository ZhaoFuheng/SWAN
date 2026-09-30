SELECT COUNT(T1.superhero_name) 
    FROM superhero AS T1 
    WHERE {{
        LLMMap(
            'Provide the race.',
            T1.superhero_name,
            options=race.race
        )
    }} = 'Vampire'
