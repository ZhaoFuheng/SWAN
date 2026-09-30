SELECT ai_classify('Which publisher publishes this superhero? superhero_name: ' || T1.superhero_name,
                   ['ABC Studios', 'DC Comics', 'Dark Horse Comics', 'George Lucas', 'Hanna-Barbera', 'HarperCollins', 'IDW Publishing', 'Icon Comics', 'Image Comics', 'J. K. Rowling', 'J. R. R. Tolkien', 'Marvel Comics', 'Microsoft', 'NBC - Heroes', 'Rebellion', 'Shueisha', 'Sony Pictures', 'South Park', 'Star Trek', 'SyFy', 'Team Epic TV', 'Titan Books', 'Universal Studios', 'Wildstorm'])
FROM superhero AS T1
WHERE T1.superhero_name = 'Blue Beetle II'
