def run(db):
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    yes = names.sem_filter("Does the hero has Super Strength? superhero_name: {superhero_name}")
    return db.sql("""
        SELECT COUNT(T1.superhero_name)
        FROM superhero AS T1
        WHERE T1.superhero_name IN (SELECT superhero_name FROM yes)
    """, yes=yes)
