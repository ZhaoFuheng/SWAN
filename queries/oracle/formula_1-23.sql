WITH race_data AS (
    SELECT *, CAST(races.year AS VARCHAR) || ' ' || races.name AS race
    FROM races
), race_month AS (
    SELECT race_data.name AS name,
        SUBSTRING(race_data.date, 6, 2) AS month
    FROM race_data
    WHERE race_data.year = 1958
)
SELECT DISTINCT race_month.name
FROM race_month
WHERE race_month.month = (SELECT MIN(race_month.month) FROM race_month)
