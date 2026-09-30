WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.School, T1.AvgScrRead,
    CASE WHEN s.Virtual = 'N'
         THEN ai_classify('Is this a magnet school, or does it offer a magnet program? school_address: ' || s.school_address,
                          ['Yes', 'No']) END AS is_magnet
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.AvgScrRead >= 600
