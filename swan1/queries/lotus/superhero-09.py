def run(db):
    options = sorted(db.table("publisher")["publisher_name"].dropna().unique())
    heroes = db.sql("SELECT superhero_name FROM superhero WHERE superhero_name = 'Blue Beetle II'")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    names = names.sem_map(
        "Provide the publisher. superhero_name: {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
        suffix="answer",
    )
    rows = heroes.merge(names, on="superhero_name", how="left")
    return rows[["answer"]].assign(answer=rows["answer"].str.strip())
