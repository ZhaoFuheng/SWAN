WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT DISTINCT s.School, T1.AvgScrRead,
    CASE WHEN s.Virtual = 'N' THEN CASE WHEN s.Magnet = 1 THEN 'Yes' ELSE 'No' END END AS is_magnet
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.AvgScrRead >= 600
