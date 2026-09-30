def run(db):
    rows = db.sql("""
        SELECT T1.NumTstTakr, T2.Street
        FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    fresno = streets.sem_filter("Is the address located in Fresno City? Street: {Street}")
    return rows[rows["Street"].isin(fresno["Street"])][["NumTstTakr"]]
