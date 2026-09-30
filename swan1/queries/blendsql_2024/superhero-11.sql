SELECT {{
    LLMMap(
        'Provide the publisher.',
        'superhero::superhero_name',
        options='publisher::publisher_name'
    )
}}
    FROM superhero
    WHERE superhero.superhero_name = 'Sauron'
