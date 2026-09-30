SELECT ai_agg(list('Italy Serie A: ' || "Italy Serie A"), 'Which country is the league Italy Serie A from?' || ' Answer with the value only, without any other words.')
FROM (SELECT 'Italy Serie A' AS "Italy Serie A")
