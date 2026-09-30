def run(db):
    rows = db.sql("""
        SELECT T2.year, circuits.location
        FROM circuits INNER JOIN races AS T2 ON T2.circuitId = circuits.circuitId
        WHERE circuits.location = 'Shanghai'
    """)
    locs = rows[["location"]].dropna().drop_duplicates()
    locs = locs.sem_map(("Provide the country name location: {location}" + " Answer with the value only, without any other words."), suffix="country")
    return rows.merge(locs, on="location", how="left")[["year", "country"]]
