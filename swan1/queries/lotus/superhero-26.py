def run(db):
    options = sorted(db.table("superpower")["power_name"].dropna().unique())
    heroes = db.sql("SELECT superhero_name FROM superhero")
    male = heroes[["superhero_name"]].dropna().drop_duplicates().sem_filter(
        "Is the hero male? superhero_name: {superhero_name}")
    heroes = heroes[heroes["superhero_name"].isin(male["superhero_name"])]
    names = heroes[["superhero_name"]].dropna().drop_duplicates()
    names = names.sem_map(
        "Provide a list of super powers (seperated by comma) for each hero. superhero_name: {superhero_name}"
        " Answer with exactly one of: " + ", ".join(options) + ".",
        suffix="powers",
    )
    names["powers"] = names["powers"].str.strip()
    # BlendSQL's splitter, run as is on sqlite
    return db.sql("""
        WITH temp_cte AS (
          SELECT heroes.superhero_name, mapped.powers
          FROM heroes LEFT JOIN mapped ON mapped.superhero_name = heroes.superhero_name
        ),
        Splitter AS (
          SELECT
            superhero_name,
            TRIM(SUBSTR(powers, 0, INSTR(powers || ',', ','))) AS power,
            TRIM(SUBSTR(powers, INSTR(powers || ',', ',') + 1)) AS remaining_powers
          FROM temp_cte
          WHERE LENGTH(powers) > 0

          UNION ALL

          SELECT
            superhero_name,
            TRIM(SUBSTR(remaining_powers, 0, INSTR(remaining_powers || ',', ','))) AS power,
            TRIM(SUBSTR(remaining_powers, INSTR(remaining_powers || ',', ',') + 1)) AS remaining_powers
          FROM Splitter
          WHERE LENGTH(remaining_powers) > 0
        )
        SELECT power FROM Splitter
        GROUP BY power
        ORDER BY COUNT(*)
        DESC LIMIT 5
    """, heroes=heroes, mapped=names)
