SELECT AVG(T1.height_cm) 
    FROM superhero AS T1 
    WHERE {{
        LLMMap(
            'Is the publisher Marvel Comics?'
            'T1::superhero_name'
        )
    }} = TRUE
