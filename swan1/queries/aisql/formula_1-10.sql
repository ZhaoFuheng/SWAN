WITH race_data AS (
    SELECT DISTINCT T1.name || ' ' || T1.year AS key
    FROM races AS T1
    INNER JOIN seasons AS T2 ON T2.year = T1.year
    WHERE T1.raceId = 901
)
SELECT ai_complete('Provide the wiki season URL. key: ' || race_data.key || ' Answer with the value only, without any other words.') AS season_url
FROM race_data
