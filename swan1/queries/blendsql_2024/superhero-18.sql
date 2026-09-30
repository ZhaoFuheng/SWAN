SELECT T1.superhero_name 
    FROM superhero AS T1
    WHERE {{
        LLMMap(
            'Does the hero has Death Touch power?'
            'T1::superhero_name'
        )
    }} = TRUE
