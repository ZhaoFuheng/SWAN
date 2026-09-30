SELECT CAST(COUNT(DISTINCT schools.School) AS REAL) / 12 
FROM schools
WHERE schools.DOC = 52 AND {{
        LLMMap(
            'Is the address located in Alameda County?',
            schools.Street
        )
    }} = TRUE AND strftime('%Y', schools.OpenDate) = '1980'
