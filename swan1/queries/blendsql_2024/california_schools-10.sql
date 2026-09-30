WITH temp AS (
    SELECT schools.School
    FROM schools
    WHERE {{
        LLMMap(
            'Is the address located in Contra Costa County?',
            'schools::Street'
        )
    }} = TRUE
)
SELECT sname 
FROM satscores
WHERE sname IN (SELECT School FROM temp)
ORDER BY satscores.NumTstTakr DESC 
LIMIT 1
