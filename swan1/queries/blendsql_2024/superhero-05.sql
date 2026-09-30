SELECT {{
    LLMQA(
        'What is the colour of Apocalypses skin?',
        (SELECT 'Apocalypses' AS superhero_name UNION SELECT superhero_name FROM superhero AS T1 WHERE T1.superhero_name = 'Apocalypse'),
        options='colour::colour'
    )
}}
