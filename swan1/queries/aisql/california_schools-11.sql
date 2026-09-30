WITH temp_cte AS (
    SELECT *,
        'District: ' || "District Name" || ' and School: ' || "School Name" AS district_school_key
    FROM frpm
),
temp2 AS (
    SELECT *,
        ai_complete('What is the school Charter Funding Type? district_school_key: ' || temp_cte.district_school_key || ' Answer with the value only, without any other words.') AS FundingType
    FROM temp_cte
)
SELECT T1.sname, temp2.FundingType
FROM satscores AS T1 INNER JOIN temp2 ON T1.cds = temp2.CDSCode
WHERE temp2."District Name" ILIKE 'Riverside%'
GROUP BY T1.sname, temp2.FundingType
HAVING CAST(SUM(T1.AvgScrMath) AS DOUBLE) / COUNT(T1.cds) > 400
