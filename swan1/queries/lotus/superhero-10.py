def run(db):
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    yes = names.sem_filter("Is the publisher Marvel Comics? superhero_name: {superhero_name}")
    return db.sql("""
        SELECT T1.full_name
        FROM superhero AS T1
        WHERE T1.superhero_name IN (SELECT superhero_name FROM yes)
        ORDER BY T1.height_cm DESC LIMIT 1
    """, yes=yes)
