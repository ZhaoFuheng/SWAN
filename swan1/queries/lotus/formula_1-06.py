def run(db):
    rows = db.sql("""
        SELECT circuits.name
        FROM circuits INNER JOIN races AS T2 ON T2.circuitId = circuits.circuitId
        WHERE circuits.name = 'Sepang International Circuit'
    """)
    names = rows[["name"]].dropna().drop_duplicates()
    names = names.sem_map(("Provide the wiki url. name: {name}" + " Answer with the value only, without any other words."), suffix="url")
    return rows.merge(names, on="name", how="left")[["url"]].drop_duplicates()
