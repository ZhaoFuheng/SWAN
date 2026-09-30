WITH temp AS (
SELECT *, {{
    LLMMap(
        'Provide the publisher.',
        'superhero::superhero_name',
        options='publisher::publisher_name'
    )
}} AS publisher_name
FROM superhero
)
SELECT SUM(CASE WHEN temp.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) - SUM(CASE WHEN temp.publisher_name = 'DC Comics' THEN 1 ELSE 0 END) 
    FROM temp
