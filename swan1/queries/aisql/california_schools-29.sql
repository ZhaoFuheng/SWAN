SELECT T1."Enrollment (Ages 5-17)"
FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
WHERE T2.EdOpsCode = 'SSS'
  AND ai_filter('Is the address located in Fremont City? Street: ' || T2.Street)
  AND T1."Academic Year" >= '2014' AND T1."Academic Year" <= '2015'
