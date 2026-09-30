WITH s AS (
    SELECT *, School || ', ' || MailStreet || ', ' || MailState || ' ' || MailZip AS mail_address
    FROM schools
)
SELECT s.MailStreet, s.MailCity
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE T1."FRPM Count (K-12)" > 2500
