WITH race_data AS (
    SELECT DISTINCT T1.year || ' ' || T1.name AS key
    FROM races AS T1
    WHERE T1.raceId = 901
)
SELECT ai_complete('Provide the wiki season URL. key: ' || race_data.key || ' Answer with the value only, without any other words.') AS season_url
FROM race_data
