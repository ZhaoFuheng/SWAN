def run(db):
    rows = db.sql("""
        SELECT frpm.CDSCode, schools.Street
        FROM frpm JOIN schools ON frpm.CDSCode = schools.CDSCode
        WHERE frpm."Free Meal Count (K-12)" > 500 AND frpm."Free Meal Count (K-12)" < 700
    """)
    streets = rows[["Street"]].dropna().drop_duplicates()
    la = streets.sem_filter("Is the address located in Los Angeles County? Street: {Street}")
    kept = rows[rows["Street"].isin(la["Street"])]
    return [(int(kept["CDSCode"].notna().sum()),)]
