def run(db):
    top = db.sql("""
        SELECT T1.AvgScrMath, schools.Street
        FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
        ORDER BY T1.NumGE1500 DESC
        LIMIT 1
    """)
    streets = top[["Street"]].dropna().drop_duplicates()
    streets = streets.sem_map(("Provide the city name based on the address. Street: {Street}" + " Answer with the value only, without any other words."), suffix="City")
    streets["City"] = streets["City"].str.strip()
    return top.merge(streets, on="Street", how="left")[["AvgScrMath", "City"]]
