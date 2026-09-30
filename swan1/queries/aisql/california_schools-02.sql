WITH temp_cte AS (
    SELECT T2.MailStreet, T2.Street
    FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
    ORDER BY T1."FRPM Count (K-12)" DESC
    LIMIT 1
)
SELECT temp_cte.MailStreet,
    (SELECT ai_agg(list('Street: ' || sub.Street), 'Provide the city name based on the address.' || ' Answer with the value only, without any other words.')
     FROM (SELECT T4.Street
           FROM frpm AS T3 INNER JOIN schools AS T4 ON T3.CDSCode = T4.CDSCode
           ORDER BY T3."FRPM Count (K-12)" DESC
           LIMIT 1) AS sub) AS City
FROM temp_cte
