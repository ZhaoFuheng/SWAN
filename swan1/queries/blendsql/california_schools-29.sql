SELECT T1.`Enrollment (Ages 5-17)` 
FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode 
WHERE T2.EdOpsCode = 'SSS' AND {{
        LLMMap(
            'Is the address located in Fremont City?',
            T2.Street
        )
    }} = TRUE AND T1.`Academic Year` >= 2014 AND T1.`Academic Year` <= 2015
