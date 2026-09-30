WITH race_data AS (
    SELECT *, T1.year || ' ' || T1.name AS key
    FROM races AS T1
    WHERE T1.year = (SELECT DISTINCT MIN(year) FROM races)
)
SELECT name
FROM race_data
WHERE {{
    LLMMap(
        'Provide the month of the race.',
        race_data.key,
        options=('1','2','3','4','5','6','7','8','9','10','11','12')
    )
}} = {{
    LLMQA(
        'Earliest month of these races?',
        (SELECT name, year FROM races WHERE year = (SELECT MIN(year) FROM races)),
        options=('1','2','3','4','5','6','7','8','9','10','11','12')
    )
}}
