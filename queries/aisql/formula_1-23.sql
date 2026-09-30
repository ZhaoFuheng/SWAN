WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), race_month AS (
    SELECT race_data.name AS name,
        ai_classify('In which month of the year was this Formula 1 race held? race: ' || race_data.race,
                    ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']) AS month
    FROM race_data
    WHERE race_data.year = 1958
)
SELECT DISTINCT race_month.name
FROM race_month
WHERE race_month.month = (SELECT MIN(race_month.month) FROM race_month)
