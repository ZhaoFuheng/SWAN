SELECT T1.full_name
    FROM superhero AS T1 
    WHERE {{
        LLMMap(
            'Is the publisher Marvel Comics?',
            T1.superhero_name
        )
    }} = TRUE
ORDER BY T1.height_cm DESC LIMIT 1
