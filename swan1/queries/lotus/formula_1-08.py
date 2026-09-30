def run(db):
    rows = db.sql("""
        SELECT constructors.name
        FROM constructorResults AS T1 INNER JOIN constructors ON constructors.constructorId = T1.constructorId
        WHERE T1.raceId = 24 AND T1.points = 1
    """)
    names = rows[["name"]].dropna().drop_duplicates()
    names = names.sem_map(("Provide the nationality. name: {name}" + " Answer with the value only, without any other words."), suffix="nationality")
    return rows.merge(names, on="name", how="left")[["nationality"]]
