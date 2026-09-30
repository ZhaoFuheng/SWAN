def run(db):
    top = db.sql("""
        SELECT T1.AvgScrMath, schools.Street
        FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
        WHERE T1.AvgScrMath IS NOT NULL
        ORDER BY T1.AvgScrMath + T1.AvgScrRead + T1.AvgScrWrite ASC
        LIMIT 1
    """)
    streets = top[["Street"]].dropna().drop_duplicates()
    streets = streets.sem_map(("Provide the county name based on the street address. Street: {Street}" + " Answer with the value only, without any other words."),
                              suffix="County")
    streets["County"] = streets["County"].str.strip()
    return top.merge(streets, on="Street", how="left")[["AvgScrMath", "County"]]
