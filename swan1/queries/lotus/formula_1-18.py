def run(db):
    # BlendSQL applies the ORDER BY / LIMIT before mapping, so only the top 10 rows are mapped
    rows = db.sql("""
        SELECT constructors.name
        FROM constructorResults AS T1 INNER JOIN constructors ON constructors.constructorId = T1.constructorId
        WHERE T1.raceId = 9
        ORDER BY T1.points DESC LIMIT 10
    """)
    names = rows[["name"]].dropna().drop_duplicates()
    names = names.sem_map(("Provide the wiki url. name: {name}" + " Answer with the value only, without any other words."), suffix="person_url")
    return rows.merge(names, on="name", how="left")[["person_url"]]
