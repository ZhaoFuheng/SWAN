def run(db):
    rows = db.sql("""
        SELECT T1.cds, schools.Street
        FROM satscores AS T1 INNER JOIN schools ON T1.cds = schools.CDSCode
        WHERE (T1.AvgScrRead + T1.AvgScrMath + T1.AvgScrWrite) >= 1500
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    lakeport = streets.sem_filter("Is the address located in Lakeport City? Street: {Street}")
    kept = rows[rows["Street"].isin(lakeport["Street"])]
    return [(int(kept["cds"].notna().sum()),)]
