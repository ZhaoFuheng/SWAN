{{
    LLMQA(
        'Where is he from?',
        (SELECT DISTINCT T2.forename || ' ' ||T2.surname 
        FROM qualifying AS T1 INNER JOIN drivers AS T2 ON T2.driverId = T1.driverId 
        WHERE T1.raceId = 347 AND T1.q2 LIKE '1:15%')
        )
}}
