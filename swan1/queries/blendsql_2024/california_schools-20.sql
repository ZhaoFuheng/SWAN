SELECT T2.School 
FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode 
WHERE {{
        LLMMap(
            'Is the school operate exclusively virtual?',
            'T2::School'
        )
    }} = TRUE
ORDER BY T1.AvgScrRead DESC LIMIT 5
