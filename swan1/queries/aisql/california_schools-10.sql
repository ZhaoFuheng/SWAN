WITH temp_cte AS (
    SELECT schools.School
    FROM schools
    WHERE ai_filter('Is the address located in Contra Costa County? Street: ' || schools.Street)
)
SELECT sname
FROM satscores
WHERE sname IN (SELECT School FROM temp_cte)
ORDER BY satscores.NumTstTakr DESC
LIMIT 1
