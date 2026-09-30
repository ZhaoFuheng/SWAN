WITH temp_cte AS (
SELECT *, {{
    LLMMap(
        'Provide the publisher.',
        superhero.superhero_name,
        options=publisher.publisher_name
    )
}} AS publisher_name
FROM superhero
)
SELECT (CAST(COUNT(*) AS REAL) * 100 / (SELECT COUNT(*) FROM superhero)), CAST(SUM(CASE WHEN temp_cte.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) AS REAL) 
    FROM temp_cte
    WHERE {{
        LLMMap(
            'Does the hero act in their own self-interest or make decisions based on their own moral code?',
            temp_cte.superhero_name
        )
    }} = TRUE
