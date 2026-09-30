-- LLMQA over (SELECT superhero_name ... = '3-D Man') with options=superpower.power_name
WITH RECURSIVE temp_cte AS (
    SELECT ai_agg(list('superhero_name: ' || superhero_name),
                  'Provide a list of super powers seperated by comma. Answer with exactly one of: '
                  || (SELECT string_agg(DISTINCT power_name, ', ' ORDER BY power_name) FROM superpower) || '.') AS powers
    FROM (SELECT superhero_name FROM superhero WHERE superhero.superhero_name = '3-D Man')
),
Splitter AS (
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
SELECT superpower FROM Splitter
