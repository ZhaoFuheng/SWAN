SELECT COUNT(T1.cds) 
 FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
WHERE (T1.AvgScrRead + T1.AvgScrMath + T1.AvgScrWrite) >= 1500 AND {{
        LLMMap(
            'Is the address located in Lakeport City?',
            'schools::Street'
        )
    }} = TRUE
