def run(db):
    rows = db.sql("""
        SELECT T2.School, T2.Street
        FROM satscores AS T1 INNER JOIN schools AS T2 ON T1.cds = T2.CDSCode
        WHERE T1.NumTstTakr > 500
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    magnet = streets.sem_filter("Is the school at the address a magnet school? Street: {Street}")
    return rows[rows["Street"].isin(magnet["Street"])][["School"]]
