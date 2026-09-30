def run(db):
    options = sorted(db.table("race")["race"].dropna().unique())
    heroes = db.sql("SELECT superhero_name FROM superhero WHERE superhero_name = 'Copycat'")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    names = names.sem_map(
        "What is the race of the hero? superhero_name: {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
        suffix="answer",
    )
    rows = heroes.merge(names, on="superhero_name", how="left")
    return rows[["answer"]].assign(answer=rows["answer"].str.strip())
