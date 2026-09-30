def run(db):
    options = sorted(db.table("publisher")["publisher_name"].dropna().unique())
    heroes = db.table("superhero")
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    mapped = names.sem_map(
        "Provide the publisher. superhero_name: {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
        suffix="publisher_name",
    )
    mapped["publisher_name"] = mapped["publisher_name"].str.strip()
    return db.sql("""
        WITH temp_cte AS (
            SELECT superhero.*, mapped.publisher_name
            FROM superhero LEFT JOIN mapped ON mapped.superhero_name = superhero.superhero_name
        )
        SELECT SUM(CASE WHEN temp_cte.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END)
             - SUM(CASE WHEN temp_cte.publisher_name = 'DC Comics' THEN 1 ELSE 0 END)
        FROM temp_cte
    """, mapped=mapped)
