def run(db):
    top = db.sql("""
        SELECT schools.Street, schools.Zip, schools.State
        FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
        ORDER BY CAST(T1.NumGE1500 AS REAL) / T1.NumTstTakr ASC
        LIMIT 10
    """)
    streets = top[["Street"]].dropna().drop_duplicates()
    streets = streets.sem_map(("Provide the city name based on the address. Street: {Street}" + " Answer with the value only, without any other words."), suffix="City")
    streets["City"] = streets["City"].str.strip()
    return top.merge(streets, on="Street", how="left")[["Street", "City", "Zip", "State"]]
