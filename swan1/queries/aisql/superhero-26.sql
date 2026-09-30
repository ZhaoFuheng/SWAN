-- sqlite's SUBSTR(s, 0, n) (n - 1 characters) is written SUBSTR(s, 1, n - 1)
WITH RECURSIVE temp_cte AS (
    SELECT *,
        ai_classify('Provide a list of super powers (seperated by comma) for each hero. superhero_name: ' || superhero.superhero_name,
                    (SELECT list(DISTINCT power_name ORDER BY power_name) FROM superpower)) AS powers
    FROM superhero
    WHERE ai_filter('Is the hero male? superhero_name: ' || superhero.superhero_name)
),
Splitter AS (
    SELECT
        superhero_name,
        TRIM(SUBSTR(powers, 1, INSTR(powers || ',', ',') - 1)) AS power,
        TRIM(SUBSTR(powers, INSTR(powers || ',', ',') + 1)) AS remaining_powers
    FROM temp_cte
    WHERE LENGTH(powers) > 0

    UNION ALL

    SELECT
        superhero_name,
        TRIM(SUBSTR(remaining_powers, 1, INSTR(remaining_powers || ',', ',') - 1)) AS power,
        TRIM(SUBSTR(remaining_powers, INSTR(remaining_powers || ',', ',') + 1)) AS remaining_powers
    FROM Splitter
    WHERE LENGTH(remaining_powers) > 0
)
SELECT power FROM Splitter
GROUP BY power
ORDER BY COUNT(*) DESC
LIMIT 5
