def run(db):
    options = sorted(db.table("race")["race"].dropna().unique())
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    names = names.sem_map(
        "Provide the race. superhero_name: {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
        suffix="race",
    )
    names["race"] = names["race"].str.strip()
    return db.sql("""
        SELECT COUNT(T1.superhero_name)
        FROM superhero AS T1 JOIN mapped ON mapped.superhero_name = T1.superhero_name
        WHERE mapped.race = 'Vampire'
    """, mapped=names)
