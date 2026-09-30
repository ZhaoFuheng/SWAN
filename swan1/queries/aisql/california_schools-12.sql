SELECT T1."School Name", T2.Zip, T2.Street,
    ai_complete('Provide the city name based on the address. Street: ' || T2.Street || ' Answer with the value only, without any other words.') AS City,
    T2.State
FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode
WHERE T1."Free Meal Count (Ages 5-17)" > 800 AND T1."School Type" = 'High Schools (Public)'
  AND ai_filter('Is the address located in Monterey County? Street: ' || T2.Street)
