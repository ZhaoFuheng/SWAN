WITH s AS (
    SELECT *, School || ', ' || Street || ', ' || State || ' ' || Zip AS school_address
    FROM schools
)
SELECT CAST(COUNT(DISTINCT CASE WHEN s.DOC = '54' THEN substr(s.CDSCode, 1, 14) END) AS DOUBLE)
       / NULLIF(COUNT(DISTINCT CASE WHEN s.DOC = '56' THEN substr(s.CDSCode, 1, 14) END), 0)
FROM satscores AS D INNER JOIN s ON s.District = D.dname
WHERE substr(s.Zip, 1, 3) IN ('926', '927', '928')
  AND D.rtype = 'D'
  AND ai_filter('Context:
[dname]: «' || D.dname || '»


Claim: Is this California school district in Orange County? dname')
  AND ai_filter('Context:
[school_address]: «' || s.school_address || '»


Claim: Is this a public high school? school_address')
  AND s.DOC IN ('54', '56')
