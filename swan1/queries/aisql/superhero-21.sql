WITH temp_cte AS (
    SELECT *,
        ai_classify('Provide the publisher. superhero_name: ' || superhero.superhero_name,
                    (SELECT list(DISTINCT publisher_name ORDER BY publisher_name) FROM publisher)) AS publisher_name
    FROM superhero
)
SELECT (CAST(COUNT(*) AS DOUBLE) * 100 / (SELECT COUNT(*) FROM superhero)),
       CAST(SUM(CASE WHEN temp_cte.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) AS DOUBLE)
FROM temp_cte
WHERE ai_filter('Does the hero act in their own self-interest or make decisions based on their own moral code? superhero_name: ' || temp_cte.superhero_name)
