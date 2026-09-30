SELECT COUNT(T1.CDSCode) 
    FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds 
    WHERE T1.StatusType = 'Merged' AND T2.NumTstTakr < 100 AND {{
        LLMMap(
        'Is the address located in Alameda County?',
        T1.Street
        )
    }} = TRUE
