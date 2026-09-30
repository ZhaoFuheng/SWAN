WITH temp_cte AS (
SELECT {{
 LLMQA (
    'Provide a list of super powers seperated by comma.',
    (SELECT superhero_name FROM superhero WHERE superhero.superhero_name = '3-D Man'),
    options=superpower.power_name
    )
}} AS powers
),
WITH Splitter AS (
    SELECT 
        TRIM(SUBSTR(powers, 1, INSTR(powers || ',', ',') - 1)) AS superpower,
        TRIM(SUBSTR(powers, INSTR(powers || ',', ',') + 1)) AS remaining
    FROM temp_cte
  
    UNION ALL
    
    SELECT 
        TRIM(SUBSTR(remaining, 1, INSTR(remaining || ',', ',') - 1)) AS superpower,
        TRIM(SUBSTR(remaining, INSTR(remaining || ',', ',') + 1)) AS remaining
    FROM Splitter
    WHERE remaining != ''
)
SELECT superpower FROM Splitter;
