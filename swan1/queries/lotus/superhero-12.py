def run(db):
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    first = names.sem_filter("Is the publisher Marvel Comics? superhero_name: {superhero_name}")
    second = names.sem_filter("Does the hero has blue eye? superhero_name: {superhero_name}")
    return db.sql("""
        SELECT COUNT(T1.id)
        FROM superhero AS T1
        WHERE T1.superhero_name IN (SELECT superhero_name FROM first)
          AND T1.superhero_name IN (SELECT superhero_name FROM second)
    """, first=first, second=second)
