SELECT CAST(SUM(CASE WHEN schools.DOC = 54 THEN 1 ELSE 0 END) AS REAL) / SUM(CASE WHEN schools.DOC = 52 THEN 1 ELSE 0 END) 
FROM schools
WHERE schools.StatusType = 'Merged' AND {{
        LLMMap(
            'Is the address located in Orange County?',
            schools.Street
        )
    }} = TRUE
