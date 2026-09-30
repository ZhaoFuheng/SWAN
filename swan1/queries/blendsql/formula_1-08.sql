SELECT {{
    LLMMap(
        'Provide the nationality.',
        constructors.name
    )
}} AS nationality
FROM constructorResults AS T1 INNER JOIN constructors ON constructors.constructorId = T1.constructorId
WHERE T1.raceId = 24 AND T1.points = 1
