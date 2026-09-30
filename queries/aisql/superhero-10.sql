SELECT T1.superhero_name, T1.full_name,
       ai_classify('Which publisher publishes this superhero? superhero_name: ' || T1.superhero_name,
                   ['ABC Studios', 'DC Comics', 'Dark Horse Comics', 'George Lucas', 'Hanna-Barbera', 'HarperCollins', 'IDW Publishing', 'Icon Comics', 'Image Comics', 'J. K. Rowling', 'J. R. R. Tolkien', 'Marvel Comics', 'Microsoft', 'NBC - Heroes', 'Rebellion', 'Shueisha', 'Sony Pictures', 'South Park', 'Star Trek', 'SyFy', 'Team Epic TV', 'Titan Books', 'Universal Studios', 'Wildstorm']) AS publisher
FROM superhero AS T1
WHERE T1.weight_kg BETWEEN 100 AND 200
  AND T1.height_cm IS NOT NULL
ORDER BY T1.height_cm DESC, T1.id
LIMIT 5
