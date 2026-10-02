WITH s AS (
    SELECT *, School || ', ' || MailStreet || ', ' || MailState || ' ' || MailZip AS mail_address
    FROM schools
)
SELECT COUNT(DISTINCT substr(T1.cds, 1, 14))
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE s.MailCity = 'Escondido'
  AND T1.AvgScrRead + T1.AvgScrMath + T1.AvgScrWrite >= 1500
