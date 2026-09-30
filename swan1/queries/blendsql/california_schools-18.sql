SELECT {{
    LLMMap (
        'Provide the school website address for each school.',
        schools.School
        )
}} AS Website
FROM satscores INNER JOIN schools ON satscores.cds = schools.CDSCode
WHERE {{
        LLMMap(
            'Is the address located in Los Angeles County?',
            schools.Street
        )
    }} = TRUE AND 1 AND satscores.NumTstTakr >= 150 AND satscores.NumTstTakr <= 160
