SELECT T2.School
FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
WHERE T1.NumTstTakr > 500 
AND {{
    LLMMap(
        'Is the school at the address a magnet school?', 
        T2.Street
        )
}} = TRUE
