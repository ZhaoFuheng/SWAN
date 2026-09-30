WITH temp_cte AS (
SELECT *, {{
 LLMMap(
    'Provide a list of super powers (seperated by comma) for each hero.',
    superhero.superhero_name,
    options=superpower.power_name
    )
}} AS powers FROM superhero WHERE {{
    LLMMap(
        'Is the hero male?',
        superhero.superhero_name
    )
}} = TRUE
),
Splitter AS (
  SELECT 
    superhero_name,
    TRIM(SUBSTR(powers, 0, INSTR(powers || ',', ','))) AS power,
    TRIM(SUBSTR(powers, INSTR(powers || ',', ',') + 1)) AS remaining_powers
  FROM temp_cte
  WHERE LENGTH(powers) > 0
  
  UNION ALL
  
  SELECT
    superhero_name,
    TRIM(SUBSTR(remaining_powers, 0, INSTR(remaining_powers || ',', ','))) AS power,
    TRIM(SUBSTR(remaining_powers, INSTR(remaining_powers || ',', ',') + 1)) AS remaining_powers
  FROM Splitter
  WHERE LENGTH(remaining_powers) > 0
)
SELECT power FROM Splitter
GROUP BY power
ORDER BY COUNT(*)
DESC LIMIT 5
