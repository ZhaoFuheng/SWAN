WITH race_data AS (
    SELECT *, T1.year || ' ' || T1.name AS key
    FROM races AS T1
    WHERE T1.year = (SELECT DISTINCT MIN(year) FROM races)
)
SELECT name
FROM race_data
WHERE ai_classify('Provide the month of the race. key: ' || race_data.key,
                  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    = (SELECT trim(ai_agg(list('name: ' || name || ', year: ' || year),
                          'Earliest month of these races? Answer with exactly one of: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12.'))
       FROM races WHERE year = (SELECT MIN(year) FROM races))
