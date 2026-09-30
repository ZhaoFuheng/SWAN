def run(db):
    rows = db.sql("""
        SELECT T1.CDSCode, T1.Street
        FROM schools AS T1 INNER JOIN satscores AS T2 ON T1.CDSCode = T2.cds
        WHERE T1.StatusType = 'Merged' AND T2.NumTstTakr < 100
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    if len(streets):
        streets = streets.sem_filter("Is the address located in Alameda County? Street: {Street}")
    kept = rows[rows["Street"].isin(streets["Street"])]
    return [(int(kept["CDSCode"].notna().sum()),)]
