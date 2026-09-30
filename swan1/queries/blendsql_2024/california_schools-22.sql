SELECT T1.AvgScrMath, {{
    LLMMap(
        'Provide the city name based on the address.',
        'schools::Street'
    )
}} AS City
FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode 
ORDER BY T1.NumGE1500 DESC LIMIT 1
