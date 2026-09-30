-- DuckDB's SUM of integers is a HUGEINT, which the JSON output writes as a string; BIGINT keeps it a number
WITH temp_cte AS (
    SELECT *,
        ai_classify('Provide the publisher. superhero_name: ' || superhero.superhero_name,
                    (SELECT list(DISTINCT publisher_name ORDER BY publisher_name) FROM publisher)) AS publisher_name
    FROM superhero
)
SELECT CAST(SUM(CASE WHEN temp_cte.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END)
          - SUM(CASE WHEN temp_cte.publisher_name = 'DC Comics' THEN 1 ELSE 0 END) AS BIGINT)
FROM temp_cte
