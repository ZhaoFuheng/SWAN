def run(db):
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    yes = names.sem_filter("Is the hero female? superhero_name: {superhero_name}")
    return db.sql("""
        SELECT AVG(T1.weight_kg)
        FROM superhero AS T1
        WHERE T1.superhero_name IN (SELECT superhero_name FROM yes)
    """, yes=yes)
