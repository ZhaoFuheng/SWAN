WITH race_data AS (
    SELECT DISTINCT T1.year || ' ' || T1.name AS key
    FROM races AS T1
    WHERE T1.raceId = 901
)
SELECT {{
    LLMMap(
        'Provide the wiki season URL.',
        'race_data::key'
    )
}} AS season_url
FROM race_data
