SELECT COUNT(T1.id) 
    FROM superhero AS T1 
    WHERE T1.height_cm > 200 AND {{
        LLMMap(
            'Does the hero has Super Strength?'
            'T1::superhero_name'
        )
    }} = TRUE
