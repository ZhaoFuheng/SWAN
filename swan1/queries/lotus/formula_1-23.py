MONTHS = [str(m) for m in range(1, 13)]
OPTIONS = " Answer with exactly one of: " + ", ".join(MONTHS) + "."


def run(db):
    race_data = db.sql("""
        SELECT name, year || ' ' || name AS key
        FROM races
        WHERE year = (SELECT DISTINCT MIN(year) FROM races)
    """)
    keys = race_data[["key"]].dropna().drop_duplicates()
    keys = keys.sem_map("Provide the month of the race. key: {key}" + OPTIONS, suffix="month")
    keys["month"] = keys["month"].str.strip()
    races = db.sql("SELECT name, year FROM races WHERE year = (SELECT MIN(year) FROM races)")
    earliest = races.sem_agg("Earliest month of these races? name: {name}, year: {year}" + OPTIONS,
                             suffix="_output")["_output"].iloc[0].strip()
    rows = race_data.merge(keys, on="key", how="left")
    return rows[rows["month"] == earliest][["name"]]
