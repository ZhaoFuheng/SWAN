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
    yes = names.sem_filter(
        "Does the hero act in their own self-interest or make decisions based on their own moral code?"
        " superhero_name: {superhero_name}")
    return db.sql("""
        WITH temp_cte AS (
            SELECT superhero.*, mapped.publisher_name
            FROM superhero LEFT JOIN mapped ON mapped.superhero_name = superhero.superhero_name
        )
        SELECT (CAST(COUNT(*) AS REAL) * 100 / (SELECT COUNT(*) FROM superhero)),
               CAST(SUM(CASE WHEN temp_cte.publisher_name = 'Marvel Comics' THEN 1 ELSE 0 END) AS REAL)
        FROM temp_cte
        WHERE temp_cte.superhero_name IN (SELECT superhero_name FROM yes)
    """, mapped=mapped, yes=yes)
