SELECT T1.`School Name`, T2.Zip, T2.Street, {{
    LLMMap('Provide the city name based on the address.',
        'T2::Street'
        )
}}, T2.State 
    FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode 
    WHERE T1.`Free Meal Count (Ages 5-17)` > 800 AND T1.`School Type` = 'High Schools (Public)' AND {{
        LLMMap(
            'Is the address located in Monterey County?',
            'schools::Street'
        )
    }} = TRUE
