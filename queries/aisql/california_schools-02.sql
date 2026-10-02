WITH s AS (
    SELECT *, School || ', ' || MailStreet || ', ' || MailState || ' ' || MailZip AS mail_address
    FROM schools
)
SELECT DISTINCT s.MailStreet,
    ai_complete('In which city is this mailing address? mail_address: ' || s.mail_address || ' Answer with the value only, without any other words.') AS MailCity
FROM frpm AS T1 INNER JOIN s ON T1.CDSCode = s.CDSCode
WHERE T1."FRPM Count (K-12)" > 2500
