WITH s AS (
    SELECT *, School || ', ' || MailStreet || ', ' || MailState || ' ' || MailZip AS mail_address
    FROM schools
)
SELECT COUNT(T1.cds)
FROM satscores AS T1 INNER JOIN s ON T1.cds = s.CDSCode
WHERE ai_filter('Is this mailing address in the city of Escondido, California? mail_address: ' || s.mail_address)
  AND T1.AvgScrRead + T1.AvgScrMath + T1.AvgScrWrite >= 1500
