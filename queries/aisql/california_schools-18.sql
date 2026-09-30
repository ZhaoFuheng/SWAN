WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT s.School, ai_complete('What is the website address of the school? school_address: ' || s.school_address || ' Answer with the value only, without any other words.') AS Website
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE T1.NumTstTakr BETWEEN 150 AND 200
  AND (ai_filter('Is the school located in Los Angeles County, California? school_address: ' || s.school_address) OR ai_filter('Is this a magnet school, or does it offer a magnet program? school_address: ' || s.school_address))
