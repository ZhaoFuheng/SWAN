SELECT T1.AvgScrMath, {{
    LLMMap(
        'Provide the county name based on the street address.',
        schools.Street
    )
}} AS County
FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode 
WHERE T1.AvgScrMath IS NOT NULL ORDER BY T1.AvgScrMath + T1.AvgScrRead + T1.AvgScrWrite ASC LIMIT 1
