WITH race_data AS (
    SELECT DISTINCT T1.name || ' ' || T1.year AS key,
    FROM races AS T1
    INNER JOIN seasons AS T2 ON T2.year = T1.year
    WHERE T1.raceId = 901
)
SELECT {{
    LLMMap(
        'Provide the wiki season URL.',
        race_data.key
    )
}} AS season_url
FROM race_data
