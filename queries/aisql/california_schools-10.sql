WITH districts AS (
    SELECT dname FROM satscores WHERE rtype = 'D'
),
orange AS (
    SELECT DISTINCT substr(T2.CDSCode, 1, 14) AS cds, T2.School, T1.NumTstTakr
    FROM districts AS D INNER JOIN schools AS T2 ON T2.District = D.dname INNER JOIN satscores AS T1 ON T1.cds = T2.CDSCode
    WHERE T1.NumTstTakr >= 100
      AND ai_filter('Context:
[dname]: «' || D.dname || '»


Claim: Is this California school district in Orange County? dname')
)
SELECT orange.School
FROM orange
ORDER BY orange.NumTstTakr DESC, orange.School, orange.cds
LIMIT 1
