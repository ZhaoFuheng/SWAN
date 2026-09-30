SELECT DISTINCT T1.full_name 
FROM superhero AS T1
WHERE {{
        LLMMap(
            'Does the hero has more than 15 different powers?'
            'T1::superhero_name'
        )
    }} = TRUE
