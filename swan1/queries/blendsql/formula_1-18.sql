SELECT {{
    LLMMap(
        'Provide the wiki url.',
        constructors.name
    )
}} AS person_url
FROM constructorResults AS T1 INNER JOIN constructors ON constructors.constructorId = T1.constructorId
WHERE T1.raceId = 9
ORDER BY T1.points DESC LIMIT 10
