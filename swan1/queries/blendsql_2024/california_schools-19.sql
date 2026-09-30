SELECT AVG(T1.NumTstTakr) 
FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode 
WHERE strftime('%Y', schools.OpenDate) = '1980' AND {{
        LLMMap(
            'Is the address located in Fresno County?',
            'schools::Street'
        )
    }} = TRUE
