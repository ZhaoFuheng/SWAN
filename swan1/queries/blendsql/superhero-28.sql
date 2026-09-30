SELECT DISTINCT T1.superhero_name 
    FROM superhero AS T1
    WHERE T1.height_cm BETWEEN 170 AND 190 AND {{
        LLMMap(
            'Doees the hero has no eye colour?',
            T1.superhero_name
        )
    }} = TRUE
