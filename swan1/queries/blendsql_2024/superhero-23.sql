SELECT {{
    LLMMap(
        'Provide the eye color.',
        'superhero::superhero_name',
        options='colour::colour'
    )

}}
FROM superhero
WHERE id = 75
