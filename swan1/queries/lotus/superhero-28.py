def run(db):
    # the relational condition is applied before the LLM call, as in BlendSQL
    heroes = db.sql("SELECT * FROM superhero AS T1 WHERE T1.height_cm BETWEEN 170 AND 190")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    yes = names.sem_filter("Doees the hero has no eye colour? superhero_name: {superhero_name}")
    return db.sql("""
        SELECT DISTINCT T1.superhero_name
        FROM superhero AS T1
        WHERE T1.height_cm BETWEEN 170 AND 190 AND T1.superhero_name IN (SELECT superhero_name FROM yes)
    """, yes=yes)
